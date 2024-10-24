import pytest
from app.users.user_profile.service import UserService


@pytest.fixture
def user_service_mock(auth_service_mock, fake_user_repository):
    return UserService(user_repository=fake_user_repository, auth_service=auth_service_mock)
