from cache.accessor import get_redis_connection
from database.accessor import get_db_session, Session
from repository.cache_task import TaskCache
from repository.task import TaskRepository
from repository.user import UserRepository
from service.auth import AuthService
from service.task import TaskService
from fastapi import Depends
from redis import Redis

from service.user import UserService


def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session)


def get_task_cache_repository(redis_connection: Redis = Depends(get_redis_connection)) -> TaskCache:
    return TaskCache(redis=redis_connection)


def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCache = Depends(get_task_cache_repository)
) -> TaskService:
    return TaskService(task_cache=task_cache,
                       task_repository=task_repository)


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=user_repository)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository)
