from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime, UTC
from database.models.notification import NotificationRoutingKey
from notification_services.notification.schemas.base_notification_context import BaseNotificationContext
from notification_services.notification.schemas.email import (
    EmailBidLostWonContext,
    EmailCodeContext,
    EmailContext,
    EmailNewBidPlacedContext,
    EmailResetCodeContext,
)
from notification_services.notification.schemas.sms import (
            SMSBidResultContext,
            SMSCodeContext,
            SMSContext,
        )


class ContextFactory(ABC):

    @abstractmethod
    def create_context(self, routing_key: str, payload: dict[str, Any],
                       notification_uuid: str) -> BaseNotificationContext:
        pass


class EmailContextFactory(ContextFactory):

    def create_context(self, routing_key: str, payload: dict[str, Any],
                       notification_uuid: str) -> EmailContext:


        def build_bid_lost_won_context():
            return EmailBidLostWonContext(
                bid_amount=payload.get("bid_amount"),
                auction_date=payload.get("auction_date"),
                vehicle_title=payload.get("vehicle_title"),
                vehicle_image=payload.get("vehicle_image"),
                auction=payload.get("auction"),
                lot_id=payload.get("lot_id"),
                final_bid=payload.get("final_bid"),
                user_uuid=payload.get("user_uuid"),
                notification_uuid=notification_uuid
            )

        context_map = {
            NotificationRoutingKey.AUTH_SEND_CODE.value: lambda: EmailCodeContext(
                code=payload.get("code"),
                expire_minutes=payload.get("expire_minutes", 15),
                year=datetime.now(UTC).year,
                user_uuid=payload.get("user_uuid"),
                notification_uuid=notification_uuid
            ),
            NotificationRoutingKey.AUTH_RESET_PASSWORD.value: lambda: EmailResetCodeContext(
                code=payload.get("code"),
                expire_minutes=payload.get("expire_minutes", 15),
                year=datetime.now(UTC).year,
                user_uuid=payload.get("user_uuid"),
                user_email=payload.get("email"),
                notification_uuid=notification_uuid
            ),
            NotificationRoutingKey.NEW_BID_PLACED.value: lambda: EmailNewBidPlacedContext(
                bid_amount=payload.get("bid_amount"),
                auction_data=payload.get("auction_data"),
                vehicle_title=payload.get("vehicle_title"),
                vehicle_image=payload.get("vehicle_image"),
                auction=payload.get("auction"),
                lot_id=payload.get("lot_id"),
                current_bid=payload.get("current_bid", 0),
                user_uuid=payload.get("user_uuid"),
                notification_uuid=notification_uuid
            ),
            NotificationRoutingKey.YOU_WON_BID.value: build_bid_lost_won_context,
            NotificationRoutingKey.YOU_LOST_BID.value: build_bid_lost_won_context
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

        def build_bid_result_context(final_bid_fallback: bool = False):
            return SMSBidResultContext(
                lot_id=payload.get("lot_id"),
                bid_amount=payload.get("bid_amount"),
                final_bid=payload.get("final_bid") or (payload.get("bid_amount") if final_bid_fallback else None),
                vehicle_title=payload.get("vehicle_title"),
                auction=payload.get("auction"),
                user_uuid=payload.get("user_uuid"),
                notification_uuid=notification_uuid
            )

        context_map = {
            NotificationRoutingKey.AUTH_SEND_CODE.value: lambda: SMSCodeContext(
                code=payload.get("code"),
                expire_minutes=payload.get("expire_minutes", 15),
                user_uuid=payload.get("user_uuid"),
                notification_uuid=notification_uuid
            ),
            NotificationRoutingKey.YOU_WON_BID.value: lambda: build_bid_result_context(final_bid_fallback=True),
            NotificationRoutingKey.YOU_LOST_BID.value: build_bid_result_context
        }

        context_creator = context_map.get(routing_key)
        if context_creator:
            return context_creator()

        return SMSContext(
            user_uuid=payload.get("user_uuid"),
            notification_uuid=notification_uuid
        )
