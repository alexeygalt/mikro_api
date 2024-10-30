import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.dependency import get_broker_consumer
from app.tasks.handlers import router as task_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await make_amqp_consumer()
#     yield

# await self.broker_consumer.consume_callback_message()

@asynccontextmanager
async def lifespan(app: FastAPI):
    broker_consumer = await get_broker_consumer()
    consumer_task = asyncio.create_task(broker_consumer.consume_callback_message())
    yield
    consumer_task.cancel()
    await broker_consumer.close_connection()


app = FastAPI(lifespan=lifespan)

app.include_router(task_router)
app.include_router(auth_router)
app.include_router(user_router)
