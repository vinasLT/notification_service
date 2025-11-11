from datetime import datetime

from config import settings
from notification_services.notification.schemas.base_notification_context import BaseNotificationContext, BaseNotification


class EmailContext(BaseNotificationContext):
    logo_url: str = settings.LOGO_URL
    user_uuid: str
    notification_uuid: str

class EmailNotification(BaseNotification):
    subject: str
    template_name: str
    context: EmailContext

class EmailBidClass(EmailContext):
    bid_amount: int
    auction_date: datetime
    vehicle_title: str
    vehicle_image: str
    auction: str
    lot_id: int

class EmailNewBidPlacedContext(EmailBidClass):
    current_bid: int

class EmailBidLostWonContext(EmailBidClass):
    final_bid: int

class EmailCodeContext(EmailContext):
    code: str
    expire_minutes: int
    year: int

class EmailResetCodeContext(EmailContext):
    code: str
    expire_minutes: int
    year: int
    user_email: str




class EmailPasswordResetContext(EmailContext):
    reset_link: str
    expire_hours: int



