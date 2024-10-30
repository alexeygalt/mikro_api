from dataclasses import dataclass
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserBaseSchema


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(self, user: UserBaseSchema) -> UserProfile:
        query = (
            insert(UserProfile).values(**user.model_dump()).returning(UserProfile.id)
        )
        async with self.db_session as session:
            user_id = (await session.execute(query)).scalar()
            await session.commit()
            await session.flush()
        return await self.get_user(user_id)

    async def get_user(self, user_id):
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()
