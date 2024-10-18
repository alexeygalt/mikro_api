from fastapi import Request, Security, HTTPException
from fastapi import security

from cache.accessor import get_redis_connection
from client.google import GoogleClient
from client.yandex import YandexClient
from database.accessor import get_db_session, Session
from exeptions import TokenNotValidException, TokenExpiredException
from repository.cache_task import TaskCache
from repository.task import TaskRepository
from repository.user import UserRepository
from service.auth import AuthService
from service.task import TaskService
from fastapi import Depends
from redis import Redis

from service.user import UserService
from settings import settings


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


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=settings)


def get_yandex_client() -> YandexClient:
    return YandexClient(settings=settings)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client)
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=settings, google_client=google_client,
                       yandex_client=yandex_client)


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_token = security.HTTPBearer()


def get_request_user_id(auth_service: AuthService = Depends(get_auth_service),
                        token: security.http.HTTPAuthorizationCredentials = Depends(reusable_token)) -> int:
    try:
        return auth_service.get_user_id_from_token(token.credentials)
    except TokenNotValidException as e:
        raise HTTPException(status_code=401, detail=e.detail)

    except TokenExpiredException as e:
        raise HTTPException(status_code=401, detail=e.detail)
