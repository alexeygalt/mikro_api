from dataclasses import dataclass
import pytest

from app.users.user_profile.schema import UserBaseSchema
from tests.fixtures.users.user_model import UserProfileFactory


@dataclass
class FakeUserRepository:
    async def get_user_by_email(self, email: str) -> None:
        return None

    async def create_user(self, user: UserBaseSchema) -> None:
        return UserProfileFactory()

    async def get_by_username(self, username: str):
        return UserProfileFactory(email='test@example.com', name='Test User', password='password', id=1)


@pytest.fixture
def fake_user_repository():
    return FakeUserRepository()


@pytest.fixture
def current_user() -> UserProfileFactory:
    return UserProfileFactory(email='test@example.com', name='Test User', password='password', id=1)
