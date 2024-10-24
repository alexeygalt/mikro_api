import pytest

from app.tasks.repository.cache_task import TaskCache


@pytest.fixture
def get_task_cache_repository(get_redis_connection):
    return TaskCache(redis=get_redis_connection)
