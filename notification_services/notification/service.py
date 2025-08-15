import asyncio
from abc import ABC, abstractmethod
from typing import Any

from notification_services.notification.configs.template_config import TemplateConfig, EmailTemplateConfig
from notification_services.notification.factories.context_factory import ContextFactory, EmailContextFactory
from notification_services.notification.schemas.email import EmailContext, EmailNotification
from notification_services.notification.schemas.sms import SMSContext, SMSNotification
from notification_services.notification.senders.send_email import send_templated_email

from notification_services.notification.senders.send_sms import send_sms


class NotificationService(ABC):

    def __init__(self, context_factory: ContextFactory, template_config: type[TemplateConfig]):
        self.context_factory = context_factory
        self.template_config = template_config

    @abstractmethod
    async def send_notification(self, payload: dict[str, Any], routing_key: str, notification_uuid: str):
        pass


class EmailNotificationService(NotificationService):

    async def send_notification(self, payload: dict[str, Any], routing_key: str, notification_uuid: str):

        email = payload.get("email")
        if not email:
            raise ValueError("Email address is required for email notifications")

        template_config = self.template_config.get_template_config(routing_key)
        context = self.context_factory.create_context(routing_key, payload, notification_uuid)

        if not isinstance(context, EmailContext):
            raise TypeError(f"Expected EmailContext, got {type(context)}")

        email_notification = EmailNotification(
            recipient=email,
            subject=template_config["subject"],
            template_name=template_config["template"],
            context=context
        )

        await send_templated_email(email_notification)


class SMSNotificationService(NotificationService):

    async def send_notification(self, payload: dict[str, Any], routing_key: str, notification_uuid: str):

        phone_number = payload.get("phone_number")
        if not phone_number:
            raise ValueError("Phone number is required for SMS notifications")

        template_config = self.template_config.get_template_config(routing_key)
        context = self.context_factory.create_context(routing_key, payload, notification_uuid)

        if not isinstance(context, SMSContext):
            raise TypeError(f"Expected SMSContext, got {type(context)}")

        message = template_config["template"].format(**context.model_dump())

        sms_notification = SMSNotification(
            recipient=phone_number,
            message=message,
            context=context
        )

        send_sms(sms_notification)

if __name__ == '__main__':
    async def main():
        payload = {
            "user_uuid": 'test-key',
            'code': '123456',
            'destination': 'email',
            'first_name': 'TEST',
            'last_name': 'user',
            'email': 'peyrovskaaa@gmail.com',
            'expire_minutes': '10',
            'phone_number': '+32554653453'
        }
        notification_service = EmailNotificationService(EmailContextFactory(), EmailTemplateConfig)
        await notification_service.send_notification(payload, routing_key="auth.reset_password", notification_uuid="test-key")
    asyncio.run(main())

