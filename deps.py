from typing import Any, AsyncGenerator

import aio_pika
from aio_pika.abc import AbstractRobustConnection

from config import settings

async def get_rabbit_connection()-> AsyncGenerator[AbstractRobustConnection, Any]:
    yield await aio_pika.connect_robust(settings.RABBITMQ_URL, login=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASSWORD)

async def get_db()-> AsyncGenerator[Any, Any]:
