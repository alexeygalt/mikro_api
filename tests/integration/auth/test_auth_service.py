from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.users.auth.service import AuthService
from app.users.user_profile.models import UserProfile
from tests.fixtures.users.user_model import EXIST_GOOGLE_USER_ID, EXIST_GOOGLE_USER_EMAIL


async def test_google_auth__success(auth_service: AuthService, get_db_session: AsyncSession):
    async with get_db_session as session:
        users = (await session.execute(select(UserProfile))).scalars().all()
        assert len(users) == 0  # no users in the database before Google authentication

    code = "fake_code"
    user = await auth_service.google_auth(code)

    async with session as session:
        users = (await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalars().all()
        assert len(users) == 1


async def test_google_auth__login_exist_user(auth_service: AuthService, get_db_session: AsyncSession):
    code = "fake_code"
    query = insert(UserProfile).values(id=101, email="test@yanxex.ru")
    # TODO: refactor this
    async with get_db_session as session:
        await session.execute(query)
        await session.commit()
        user = await auth_service.google_auth(code)

    async with get_db_session as session:
        login_user = (
            await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalar_one_or_none()

    assert login_user.id == 1


async def test_base_login_success(auth_service: AuthService, get_db_session: AsyncSession):
    test_username = "test_username"
    test_password = "test_password"

    async with get_db_session as session:
        user_id = (await session.execute(
            insert(UserProfile).values(username=test_username, password=test_password).returning(
                UserProfile.id))).scalar()
        await session.commit()

    user = await auth_service.login(test_username, test_password)

    assert user.user_id == user_id
