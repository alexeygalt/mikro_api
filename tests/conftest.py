import pytest
import asyncio
import os
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.accessor import engine, AsyncSessionFactory
from app.infrastructure.database.database import Base
from app.settings import settings
from redis import asyncio as redis

os.environ["MODE"] = "TEST"

pytest_plugins = [
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.auth.clients",
    "tests.fixtures.users.user_repository",
    "tests.fixtures.users.user_model",
    "tests.fixtures.users.user_service",
    "tests.fixtures.settings",
    "tests.infrastructure",
    "tests.fixtures.tasks.tasks_service",
    "tests.fixtures.tasks.tasks_repository",
    "tests.fixtures.tasks.tasks_cache",
]


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def get_db_session():
    async with AsyncSessionFactory() as session:
        yield session


# @pytest.fixture(autouse=True)
# async def clean_db(get_db_session: AsyncSession):
#     async with get_db_session.begin():
#         for table in Base.metadata.sorted_tables:
#             await get_db_session.execute(delete(table))
#         await get_db_session.commit()


@pytest.fixture(scope="function")
async def get_redis_connection():
    connection = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    yield connection
    await connection.close()