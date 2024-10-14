from cache.accessor import get_redis_connection
from database.database import get_db_session
from repository.cache_task import TaskCache
from repository.task import TaskRepository
from service.task import TaskService
from fastapi import Depends


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_task_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis=redis_connection)


def get_task_service(
        task_repository: Depends(get_tasks_repository),
        task_cache: Depends(get_task_cache_repository)
) -> TaskService:
    return TaskService(task_cache=task_cache,
                       task_repository=task_repository)
