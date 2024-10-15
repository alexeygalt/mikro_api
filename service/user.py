import string
from dataclasses import dataclass
import random
from repository.user import UserRepository
from schema.user import UserLoginSchema


@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user(username, password, access_token=self._generate_access_token())
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_access_token() -> str:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
