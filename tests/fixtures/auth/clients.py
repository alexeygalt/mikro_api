from dataclasses import dataclass
import pytest
from faker import Factory as FakerFactory
from app.settings import settings, Settings
from app.users.auth.schema import GoogleUserData, YandexUserData
from tests.fixtures.users.user_model import EXIST_GOOGLE_USER_EMAIL, EXIST_GOOGLE_USER_ID

faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    settings: Settings

    async def get_user_info(self, code: str) -> GoogleUserData:
        print(google_user_info_data())
        return google_user_info_data()

    async def _get_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"


class FakeYandexClient(FakeGoogleClient):
    settings: Settings

    async def get_user_info(self, code: str) -> YandexUserData:
        return yandex_user_info_data()

    async def _get_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def yandex_client():
    return FakeYandexClient(settings=settings)


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=settings)


# @pytest.fixture
def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=EXIST_GOOGLE_USER_ID,
        email=EXIST_GOOGLE_USER_EMAIL,
        name=faker.name(),
        verified_email=True,
        access_token=faker.sha256())


def yandex_user_info_data() -> YandexUserData:
    return YandexUserData(
        id=faker.random_int(),
        default_email=faker.email(),
        login=faker.name(),
        real_name=faker.name(),
        access_token=faker.sha256())
