from dataclasses import dataclass
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserBaseSchema


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, user: UserBaseSchema) -> UserLoginSchema:
        user = await self.user_repository.create_user(user=user)
        access_token = self.auth_service.generate_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
