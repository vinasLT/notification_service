from pydantic import BaseModel

from config import settings


class EmailContext(BaseModel):
    company_name: str = settings.COMPANY_NAME
    link: str = f'https://{settings.COMPANY_LINK}'
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



