from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from database.models.notification import NotificationDestination, NotificationStatus, NotificationRoutingKey


class NotificationCreate(BaseModel):
    user_uuid: str
    uuid_key: str
    destination: NotificationDestination
    status: NotificationStatus
    routing_key: NotificationRoutingKey
    created_at: Optional[datetime] = None


class NotificationUpdate(BaseModel):
    user_uuid: Optional[str] = None
    uuid_key: Optional[str] = None
    destination: Optional[NotificationDestination] = None
    status: Optional[NotificationStatus] = None
    routing_key: Optional[NotificationRoutingKey] = None
    created_at: Optional[datetime] = None


class NotificationRead(NotificationCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)