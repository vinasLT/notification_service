from abc import ABC, abstractmethod
from typing import Dict
from database.models.notification import NotificationPurpose


class TemplateConfig(ABC):

    @classmethod
    @abstractmethod
    def get_template_config(cls, routing_key: str) -> Dict[str, str]:
        pass


class EmailTemplateConfig(TemplateConfig):
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


class SMSTemplateConfig(TemplateConfig):

    TEMPLATES = {
        NotificationPurpose.AUTH_SEND_CODE.value: {
            "template": "Your code: {code}. Valid for {expire_minutes} minutes.",
        }
    }

    @classmethod
    def get_template_config(cls, routing_key: str) -> Dict[str, str]:
        return cls.TEMPLATES.get(routing_key, {
            "template": "Notification from {company_name}"
        })