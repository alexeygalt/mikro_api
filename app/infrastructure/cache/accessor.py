from redis import asyncio as redis
from app.settings import settings


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
    )
