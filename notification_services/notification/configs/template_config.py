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
        },
        NotificationRoutingKey.NEW_BID_PLACED.value: {
            "template": "new_bid_placed.html",
            "subject": "New bid placed"
        },
        NotificationRoutingKey.YOU_WON_BID.value: {
            "template": "bid_won.html",
            "subject": "Congratulations! You won the auction"
        },
        NotificationRoutingKey.YOU_LOST_BID.value: {
            "template": "bid_lost.html",
            "subject": "Update on your recent bid"
        },
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
        },
        NotificationRoutingKey.YOU_WON_BID.value: {
            "template": "Congrats! You won lot #{lot_id} with a bid of ${final_bid}. Check your dashboard to complete the purchase.",
        },
        NotificationRoutingKey.YOU_LOST_BID.value: {
            "template": "Lot #{lot_id} was sold for ${final_bid}. Your top bid was ${bid_amount}. Keep watching new lots in {auction}.",
        }
    }

    @classmethod
    def get_template_config(cls, routing_key: str) -> Dict[str, str]:
        return cls.TEMPLATES.get(routing_key, {
            "template": "Notification from {company_name}"
        })
