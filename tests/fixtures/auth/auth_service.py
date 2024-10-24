import pytest
from app.settings import settings
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest.fixture
def auth_service_mock(yandex_client, google_client, fake_user_repository):
    return AuthService(user_repository=fake_user_repository, settings=settings, google_client=google_client,
                       yandex_client=yandex_client)


@pytest.fixture
def auth_service(yandex_client, google_client, auth_service_mock, get_db_session, settings):
    return AuthService(user_repository=UserRepository(db_session=get_db_session),
                       yandex_client=yandex_client,
                       google_client=google_client,
                       settings=settings)
