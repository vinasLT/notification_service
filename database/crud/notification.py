from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.base import BaseService
from database.models.notification import Notification
from database.schemas.notification import NotificationCreate, NotificationUpdate


class NotificationService(BaseService[Notification, NotificationCreate, NotificationUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Notification, session)