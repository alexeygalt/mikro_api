from dataclasses import dataclass
from exeptions import UserNotFoundException, UserNotCorrectPasswordException, TokenExpiredException, \
    TokenNotValidException
from models.user import UserProfile
from repository.user import UserRepository
from schema.user import UserLoginSchema
from jose import jwt, JWTError
import datetime as dt
from datetime import timedelta

from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

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
