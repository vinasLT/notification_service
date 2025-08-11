from contextlib import asynccontextmanager

import uvicorn
from aio_pika import connect_robust
from fastapi import FastAPI

from config import settings
from core.logger import logger
from database.db.session import get_db
from database.models.notification import NotificationPurpose
from rabbit_service.custom_consumer import RabbitNotificationConsumer


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(f"{settings.APP_NAME} started!")
    connection = await connect_robust(settings.RABBITMQ_URL)
    db = await get_db()

    consumer = RabbitNotificationConsumer(connection, db, [member.value for member in NotificationPurpose])
    await consumer.set_up()
    await consumer.start_consuming()
    yield

    await consumer.stop_consuming()


app = FastAPI(title='Notification Service',
              description='Receive events from rabbitmq and send notifications to users',
              version='0.0.1',
              lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)