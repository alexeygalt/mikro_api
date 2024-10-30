import uuid
from dataclasses import dataclass
from app.broker.producer import BrokerProducer
from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings
    broker_producer: BrokerProducer

    async def send_welcome_email(self, to: str) -> None:
        # connection = await aio_pika.connect_robust(self.settings.AMQP_URL)
        email_body = {
            "message": "Welcome to mikro",
            "email": to,
            "subject": "Welcome",
            "correlation_id": str(uuid.uuid4()),
        }
        await self.broker_producer.send_welcome_email(email_data=email_body)
        return

        # amqp
        # async with connection:
        #     channel = await connection.channel()
        #
        #     await channel.declare_queue('email_queue', durable=True)
        #     message = aio_pika.Message(
        #         body=json.dumps(email_body).encode("utf-8"),
        #         correlation_id=str(uuid.uuid4()),
        #         reply_to='callback_mail_queue'
        #     )
        #     await channel.default_exchange.publish(
        #         message=message,
        #         routing_key='email_queue'
        #     )
