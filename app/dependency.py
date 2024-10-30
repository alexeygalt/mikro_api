import json
from fastapi import HTTPException
from fastapi import security
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.broker.consumer import BrokerConsumer
from app.broker.producer import BrokerProducer
from app.tasks.repository.task import TaskRepository
from app.tasks.service import TaskService
from app.users.auth.client.google import GoogleClient
from app.exeptions import TokenExpiredException, TokenNotValidException
from app.infrastructure.cache.accessor import get_redis_connection
from app.users.auth.client.mail import MailClient
from app.users.auth.client.yandex import YandexClient
from app.infrastructure.database.accessor import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.repository.cache_task import TaskCache
from fastapi import Depends
from redis import Redis
from app.settings import settings, Settings
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.service import UserService
from aiokafka.util import get_running_loop


async def get_tasks_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> TaskRepository:
    return TaskRepository(db_session)


async def get_task_cache_repository(
    redis_connection: Redis = Depends(get_redis_connection),
) -> TaskCache:
    return TaskCache(redis=redis_connection)


async def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_task_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    task_cache: TaskCache = Depends(get_task_cache_repository),
) -> TaskService:
    return TaskService(task_cache=task_cache, task_repository=task_repository)


async def get_google_client() -> GoogleClient:
    return GoogleClient(settings=settings)


async def get_yandex_client() -> YandexClient:
    return YandexClient(settings=settings)


async def get_broker_producer() -> BrokerProducer:
    settings = Settings()
    return BrokerProducer(
        producer=AIOKafkaProducer(
            bootstrap_servers=settings.BROKER_URL, loop=get_running_loop()
        ),
        email_topic=settings.EMAIL_TOPIC,
    )


async def get_broker_consumer() -> BrokerConsumer:
    settings = Settings()
    return BrokerConsumer(
        consumer=AIOKafkaConsumer(
            "callback_email_topic",
            bootstrap_servers=settings.BROKER_URL,
            value_deserializer=lambda message: json.loads(message.decode("utf-8")),
        ),
        email_callback_topic=settings.EMAIL_CALLBACK_TOPIC,
    )


async def get_mail_client(
    broker_producer: BrokerProducer = Depends(get_broker_producer),
    # broker_consumer: BrokerConsumer = Depends(get_broker_consumer)
) -> MailClient:
    return MailClient(settings=settings, broker_producer=broker_producer)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client),
    mail_client: MailClient = Depends(get_mail_client),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=mail_client,
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_token = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Depends(reusable_token),
) -> int:
    try:
        return auth_service.get_user_id_from_token(token.credentials)
    except TokenNotValidException as e:
        raise HTTPException(status_code=401, detail=e.detail)

    except TokenExpiredException as e:
        raise HTTPException(status_code=401, detail=e.detail)
