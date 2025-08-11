from typing import Dict

from pydantic import BaseModel

from config import settings
from database.models.notification import NotificationPurpose


class EmailContext(BaseModel):
    company_name: str = settings.COMPANY_NAME
    link: str = f'https://{settings.DOMAIN}'
    logo_url: str = settings.LOGO_URL
    user_uuid: str
    notification_uuid: str


class EmailNotification(BaseModel):
    recipient: str
    subject: str
    template_name: str
    context: EmailContext

class EmailCodeContext(EmailContext):
    code: str
    expire_minutes: int
    year: int



