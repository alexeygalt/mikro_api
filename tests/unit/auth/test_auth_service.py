from app.exeptions import UserNotCorrectPasswordException
from app.settings import Settings
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from jose import jwt
import datetime as dt
import pytest

from tests.fixtures.users.user_model import UserProfileFactory


async def test_get_google_redirect_url__success(auth_service_mock: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url

    auth_service_google_redirect_url = auth_service_mock.get_google_redirect_url()

    assert settings_google_redirect_url == auth_service_google_redirect_url


async def test_get_yandex_redirect_url__success(auth_service_mock: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url

    auth_service_yandex_redirect_url = auth_service_mock.get_yandex_redirect_url()

    assert settings_yandex_redirect_url == auth_service_yandex_redirect_url


async def test_get_google_redirect_url__fail(auth_service_mock: AuthService):
    fake_google_redirect_url = "https://fake.google.com"

    auth_service_google_redirect_url = auth_service_mock.get_google_redirect_url()

    assert fake_google_redirect_url != auth_service_google_redirect_url


async def test_generate_access_token__success(auth_service_mock: AuthService):
    user_id = 1

    access_token = auth_service_mock.generate_access_token(user_id)
    decoded_access_token = jwt.decode(access_token, auth_service_mock.settings.JWT_SECRET_KEY, )
    decoded_user_id = decoded_access_token.get('user_id')
    decoded_user_expire = dt.datetime.fromtimestamp(decoded_access_token.get('expire'), tz=dt.timezone.utc)

    assert (decoded_user_expire - dt.datetime.now(tz=dt.UTC)) < dt.timedelta(minutes=30)
    assert decoded_user_id == user_id


async def test_get_user_id_from_token__success(auth_service_mock: AuthService):
    user_id = 1

    access_token = auth_service_mock.generate_access_token(user_id)
    user_id_from_token = auth_service_mock.get_user_id_from_token(access_token)

    assert user_id_from_token == user_id


async def test_google_auth__success(auth_service_mock: AuthService):
    code = "fake_code"

    user = await auth_service_mock.google_auth(code=code)
    user_id = user.user_id
    access_token = user.access_token
    decoded_user_id = auth_service_mock.get_user_id_from_token(access_token)

    assert isinstance(user, UserLoginSchema)
    assert user_id == decoded_user_id


async def test_yandex_auth__success(auth_service_mock: AuthService):
    code = "fake_code"

    user = await auth_service_mock.yandex_auth(code=code)
    user_id = user.user_id
    access_token = user.access_token
    decoded_user_id = auth_service_mock.get_user_id_from_token(access_token)

    assert isinstance(user, UserLoginSchema)
    assert user_id == decoded_user_id


async def test_login__success(auth_service_mock: AuthService, current_user):
    # current_user =UserProfileFactory(email='test@example.com', name='Test User', password='password', id=1)
    user = await auth_service_mock.login(username=current_user.username, password=current_user.password)

    assert user.user_id is not None
    assert isinstance(user, UserLoginSchema)
    assert current_user.id == user.user_id


async def test_login__fail(auth_service_mock: AuthService, current_user):
    with pytest.raises(UserNotCorrectPasswordException):
         await auth_service_mock.login(username=current_user.username, password="test")


