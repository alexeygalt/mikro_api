import factory
from faker import Factory as FakerFactory
from pytest_factoryboy import register
from app.users.user_profile.models import UserProfile
import pytest
from sqlalchemy import insert

faker = FakerFactory.create()

EXIST_GOOGLE_USER_ID = 100
EXIST_GOOGLE_USER_EMAIL = "test@gmail.com"


@register(_name='user_profile')
class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())
    yandex_access_token = factory.LazyFunction(lambda: faker.sha256())
    google_access_token = factory.LazyFunction(lambda: faker.sha256())




# @pytest.fixture
# async def get_custom_user(get_db_session):
#     query = insert(UserProfile).values(id=EXIST_GOOGLE_USER_ID, email=EXIST_GOOGLE_USER_EMAIL)
#
#     async with get_db_session as session:
#         await session.execute(query)
#         await session.commit()