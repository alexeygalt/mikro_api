from dataclasses import dataclass
from app.users.auth.client.google import GoogleClient
from app.users.auth.client.mail import MailClient
from app.users.auth.client.yandex import YandexClient
from app.exeptions import UserNotFoundException, UserNotCorrectPasswordException, TokenExpiredException, \
    TokenNotValidException
from jose import jwt, JWTError
import datetime as dt
from datetime import timedelta
from app.settings import Settings
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient
    mail_client: MailClient

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    def get_google_redirect_url(self):
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self):
        return self.settings.yandex_redirect_url

    async def google_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.google_client.get_user_info(code)
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(google_access_token=user_data.access_token, email=user_data.email,
                                            name=user_data.name)
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(created_user.id)
        await self.mail_client.send_welcome_email(to=user_data.email)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.yandex_client.get_user_info(code)

        if user := await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(yandex_access_token=user_data.access_token, email=user_data.default_email,
                                            name=user_data.name)
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(created_user.id)
        await self.mail_client.send_welcome_email(to=user_data.default_email)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (dt.datetime.now() + timedelta(minutes=30)).timestamp()
        token = jwt.encode({'user_id': user_id,
                            'expire': expires_date_unix},
                           self.settings.JWT_SECRET_KEY,
                           algorithm=self.settings.JWT_ENCODE_ALGORITHM)

        return token

    def get_user_id_from_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY,
                                 algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotValidException

        if payload['expire'] < dt.datetime.now().timestamp():
            raise TokenExpiredException
        return payload['user_id']
