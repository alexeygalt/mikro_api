from dataclasses import dataclass
from aiokafka import AIOKafkaConsumer


@dataclass
class BrokerConsumer:
    consumer: AIOKafkaConsumer
    email_callback_topic: str

    async def open_connection(self) -> None:
        await self.consumer.start()

    async def close_connection(self) -> None:
        await self.consumer.stop()

    async def consume_callback_message(self) -> None:

        await self.open_connection()
        try:
            async for message in self.consumer:
                print(message.value)
        finally:
            await self.close_connection()


# amqp

# async def make_amqp_consumer():
#     connection = await get_broker_connection()
#     channel = await connection.channel()
#     queue = await channel.declare_queue("callback_mail_queue", durable=True)
#     await queue.consume(consume_fail_email)
#
#
# async def consume_fail_email(message: aio_pika.abc.AbstractIncomingMessage):
#     async with message.process():
#         email_body = message.body.decode('utf-8')
#         correlation_id = message.correlation_id
#         print(email_body, correlation_id)
