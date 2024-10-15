from dataclasses import dataclass

from exeptions import UserNotFoundException, UserNotCorrectPasswordException
from models.user import UserProfile
from repository.user import UserRepository
from schema.user import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_by_username(username)
        self._validate_auth_user(user, password)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
