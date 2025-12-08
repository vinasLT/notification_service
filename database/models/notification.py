import enum
from datetime import datetime, UTC
from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class NotificationDestination(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    TELEGRAM = "telegram"

class NotificationStatus(str, enum.Enum):
    SUCCESS = "success"
    IN_PROGRESS = "in_progress"
    FAILURE = "failure"

class NotificationRoutingKey(str, enum.Enum):
    AUTH_SEND_CODE = "auth.send_code"
    AUTH_RESET_PASSWORD = "auth.reset_password"
    NEW_BID_PLACED = "bid.new_bid_placed"
    YOU_WON_BID = "bid.you_won_bid"
    YOU_LOST_BID = "bid.you_lost_bid"

    ORDER_STATUS_UPDATED = "order.status_updated"


class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_uuid: Mapped[str] = mapped_column(String, nullable=False)
    uuid_key: Mapped[str] = mapped_column(String, nullable=False)
    destination: Mapped[NotificationDestination] = mapped_column(
        Enum(NotificationDestination), nullable=False
    )
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus), nullable=False
    )

    routing_key: Mapped[NotificationRoutingKey] = mapped_column(Enum(NotificationRoutingKey), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now(UTC)
    )
