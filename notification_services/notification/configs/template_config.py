from abc import ABC, abstractmethod
from typing import Dict
from database.models.notification import NotificationRoutingKey


class TemplateConfig(ABC):

    @classmethod
    @abstractmethod
    def get_template_config(cls, routing_key: str) -> Dict[str, str]:
        pass


class EmailTemplateConfig(TemplateConfig):
    TEMPLATES = {
        NotificationRoutingKey.AUTH_SEND_CODE.value: {
            "template": "code_email.html",
            "subject": "Your verification code"
        },
        NotificationRoutingKey.AUTH_RESET_PASSWORD.value: {
            "template": "auth_reset_password.html",
            "subject": "Reset password code"
        }
    }

    @classmethod
    def get_template_config(cls, routing_key: str) -> Dict[str, str]:
        return cls.TEMPLATES.get(routing_key, {
            "template": "default_email.html",
            "subject": "Notification"
        })


class SMSTemplateConfig(TemplateConfig):

    TEMPLATES = {
        NotificationRoutingKey.AUTH_SEND_CODE.value: {
            "template": "Your code: {code}. Valid for {expire_minutes} minutes.",
        },
        NotificationRoutingKey.AUTH_RESET_PASSWORD.value: {
            "template": "Your code: {code}. Valid for {expire_minutes} minutes.\n"
                        "If you dont request this code ignore this message",
        }
    }

    @classmethod
    def get_template_config(cls, routing_key: str) -> Dict[str, str]:
        return cls.TEMPLATES.get(routing_key, {
            "template": "Notification from {company_name}"
        })