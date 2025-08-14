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

class EmailCodeContext(EmailContext):
    code: str
    expire_minutes: int
    year: int


class EmailPasswordResetContext(EmailContext):
    reset_link: str
    expire_hours: int



