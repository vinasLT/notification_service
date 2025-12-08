from typing import Optional

from notification_services.notification.schemas.base_notification_context import BaseNotificationContext, BaseNotification


class SMSContext(BaseNotificationContext):
    user_uuid: str
    notification_uuid: str

class SMSNotification(BaseNotification):
    message: str
    context: SMSContext

class SMSCodeContext(SMSContext):
    code: str
    expire_minutes: int


class SMSBidResultContext(SMSContext):
    lot_id: int
    bid_amount: int
    final_bid: Optional[int] = None
    vehicle_title: Optional[str] = None
    auction: Optional[str] = None


class SMSOrderStatusContext(SMSContext):
    new_order_status: str
    previous_order_status: str
    order_id: int
    vin: str
    vehicle_title: str
    auction: str
    lot_id: int
