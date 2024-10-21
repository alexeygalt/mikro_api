from dataclasses import dataclass
from app.repository.user import UserRepository
from app.schema.user import UserLoginSchema, UserBaseSchema
from app.service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, user: UserBaseSchema) -> UserLoginSchema:
        user = await self.user_repository.create_user(user=user)
        access_token = self.auth_service.generate_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
