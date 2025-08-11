import json
import uuid
from datetime import datetime, UTC
from typing import Dict, Any

from aio_pika.abc import AbstractIncomingMessage

from core.logger import logger
from database.crud.notification import NotificationService
from database.models.notification import NotificationStatus, NotificationPurpose
from database.schemas.notification import NotificationCreate, NotificationUpdate
from rabbit_service.base import RabbitBaseService
from schemas import EmailNotification, EmailCodeContext, EmailContext
from send_email import send_templated_email


class EmailTemplateConfig:
    TEMPLATES = {
        NotificationPurpose.AUTH_SEND_CODE.value: {
            "template": "code_email.html",
            "subject": "Your verification code"
        }
    }

    @classmethod
    def get_template_config(cls, routing_key: str) -> Dict[str, str]:
        return cls.TEMPLATES.get(routing_key, {
            "template": "default_email.html",
            "subject": "Notification"
        })

class EmailContextFactory:
    @staticmethod
    def create_context(routing_key: str, payload: Dict[str, Any], notification_uuid: str) -> EmailContext:
        if routing_key == NotificationPurpose.AUTH_SEND_CODE.value:
            return EmailCodeContext(
                code=payload.get("code"),
                expire_minutes=payload.get("expire_minutes", 15),
                year=datetime.now(UTC).year,
                user_uuid=payload.get("user_uuid"),
                notification_uuid=notification_uuid
            )
        else:
            return EmailContext(
                link=payload.get("link", "#")
            )


class RabbitNotificationConsumer(RabbitBaseService):

    async def process_message(self, message: AbstractIncomingMessage):

        message_data = message.body.decode("utf-8")
        payload = json.loads(message_data).get("payload")
        routing_key = message.routing_key

        logger.info("Received new message", extra = {"payload": payload})

        notification_service = NotificationService(self.db)


        user_uuid = payload.get("user_uuid")
        destination = payload.get("destination")

        logger.info("Processing email notification", extra={
            "routing_key": routing_key,
            "user_uuid": payload.get("user_uuid")
        })

        try:
            purpose = NotificationPurpose(routing_key)
        except ValueError:
            logger.error("Invalid notification purpose(routing_key)", extra={"routing_key": routing_key})
            raise

        data = NotificationCreate(user_uuid=user_uuid, uuid_key=str(uuid.uuid4()),
                                  destination=destination, status=NotificationStatus.IN_PROGRESS,
                                  purpose=purpose)
        notification_obj = await notification_service.create(data)


        if payload.get("destination") == "email":
            await self._send_email_notification(payload, routing_key, notification_obj.uuid_key)


        update_data = NotificationUpdate(status=NotificationStatus.SUCCESS)
        await notification_service.update(notification_obj.id, update_data)


    async def _send_email_notification(self, payload: Dict[str, Any], routing_key: str, notification_uuid: str):
        email = payload.get("email")
        if not email:
            logger.error("Email address is required for email notifications", extra={"payload": payload})
            raise ValueError("Email address is required for email notifications")

        template_config = EmailTemplateConfig.get_template_config(routing_key)

        context = EmailContextFactory.create_context(routing_key, payload, notification_uuid)
        print(context)

        email_notification = EmailNotification(
            recipient=email,
            subject=template_config["subject"],
            template_name=template_config["template"],
            context=context
        )

        await send_templated_email(email_notification)






