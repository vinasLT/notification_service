import enum
from datetime import datetime, UTC
from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class NotificationDestination(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"

class NotificationStatus(str, enum.Enum):
    SUCCESS = "success"
    IN_PROGRESS = "in_progress"
    FAILURE = "failure"

class NotificationPurpose(str, enum.Enum):
    AUTH_SEND_CODE = "auth.send_code"


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

    purpose: Mapped[NotificationPurpose] = mapped_column(Enum(NotificationPurpose), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now(UTC)
    )