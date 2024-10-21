from app.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(url=settings.get_db_uri)
AsyncSessionFactory = async_sessionmaker(
    engine, autocommit=False, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
