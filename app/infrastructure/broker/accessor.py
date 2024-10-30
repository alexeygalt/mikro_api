from app.settings import Settings
import aio_pika


async def get_broker_connection() -> aio_pika.abc.AbstractConnection:
    settings = Settings()
    return await aio_pika.connect_robust(settings.AMQP_URL)
