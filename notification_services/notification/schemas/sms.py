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
