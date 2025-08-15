from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime, UTC
from database.models.notification import NotificationPurpose
from notification_services.notification.schemas.base_notification_context import BaseNotificationContext
from notification_services.notification.schemas.email import EmailCodeContext, EmailContext, EmailResetCodeContext
from notification_services.notification.schemas.sms import SMSContext



class ContextFactory(ABC):

    @abstractmethod
    def create_context(self, routing_key: str, payload: dict[str, Any],
                       notification_uuid: str) -> BaseNotificationContext:
        pass


class EmailContextFactory(ContextFactory):

    def create_context(self, routing_key: str, payload: dict[str, Any],
                       notification_uuid: str) -> EmailContext:


        context_map = {
            NotificationPurpose.AUTH_SEND_CODE.value: lambda: EmailCodeContext(
                code=payload.get("code"),
                expire_minutes=payload.get("expire_minutes", 15),
                year=datetime.now(UTC).year,
                user_uuid=payload.get("user_uuid"),
                notification_uuid=notification_uuid
            ),
            NotificationPurpose.AUTH_RESET_PASSWORD.value: lambda: EmailResetCodeContext(
                code=payload.get("code"),
                expire_minutes=payload.get("expire_minutes", 15),
                year=datetime.now(UTC).year,
                user_uuid=payload.get("user_uuid"),
                user_email=payload.get("email"),
                notification_uuid=notification_uuid
            )
        }

        context_creator = context_map.get(routing_key)
        if context_creator:
            return context_creator()

        return EmailContext(
            user_uuid=payload.get("user_uuid"),
            notification_uuid=notification_uuid
        )


class SMSContextFactory(ContextFactory):
    def create_context(self, routing_key: str, payload: dict[str, Any],
                       notification_uuid: str) -> SMSContext:
        from notification_services.notification.schemas.sms import SMSCodeContext, SMSContext

        context_map = {
            NotificationPurpose.AUTH_SEND_CODE.value: lambda: SMSCodeContext(
                code=payload.get("code"),
                expire_minutes=payload.get("expire_minutes", 15),
                user_uuid=payload.get("user_uuid"),
                notification_uuid=notification_uuid
            )
        }

        context_creator = context_map.get(routing_key)
        if context_creator:
            return context_creator()

        return SMSContext(
            user_uuid=payload.get("user_uuid"),
            notification_uuid=notification_uuid
        )