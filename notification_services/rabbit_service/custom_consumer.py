import json
import traceback
import uuid

from aio_pika.abc import AbstractIncomingMessage

from core.logger import logger
from database.crud.notification import NotificationService as DBNotificationService
from database.models.notification import NotificationStatus, NotificationRoutingKey, NotificationDestination
from database.schemas.notification import NotificationUpdate, NotificationCreate
from notification_services.notification.registry import NotificationRegistry
from notification_services.rabbit_service.base import RabbitBaseService


class RabbitNotificationConsumer(RabbitBaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification_registry = NotificationRegistry()

    async def process_message(self, message: AbstractIncomingMessage):
        message_data = message.body.decode("utf-8")
        payload = json.loads(message_data).get("payload")
        routing_key = message.routing_key

        logger.info("Received new message", extra={"payload": payload})

        notification_service = DBNotificationService(self.db)
        user_uuid = payload.get("user_uuid")
        destination_str = payload.get("destination")

        logger.info("Processing notification", extra={
            "routing_key": routing_key,
            "user_uuid": user_uuid,
            "destination": destination_str
        })

        try:
            purpose = NotificationRoutingKey(routing_key)
            destination = NotificationDestination(destination_str)
        except ValueError as e:
            logger.error("Invalid notification routing_key or destination", extra={
                "routing_key": routing_key,
                "destination": destination_str,
                "error": str(e)
            })
            raise

        data = NotificationCreate(
            user_uuid=user_uuid,
            uuid_key=str(uuid.uuid4()),
            destination=destination,
            status=NotificationStatus.IN_PROGRESS,
            routing_key=purpose
        )
        notification_obj = await notification_service.create(data)

        try:
            service = self.notification_registry.get_service(destination)
            await service.send_notification(payload, routing_key, notification_obj.uuid_key)

            update_data = NotificationUpdate(status=NotificationStatus.SUCCESS)
            logger.info("Notification sent successfully", extra={
                "notification_uuid": notification_obj.uuid_key,
                "destination": destination_str
            })

        except Exception as e:
            traceback.print_exc()
            logger.exception("Failed to send notification", extra={
                "notification_uuid": notification_obj.uuid_key,
                "destination": destination_str,
                "error": str(e)

            })
            update_data = NotificationUpdate(status=NotificationStatus.FAILURE)

        await notification_service.update(notification_obj.id, update_data)









