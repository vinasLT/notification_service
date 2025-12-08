from database.models.notification import NotificationDestination
from notification_services.notification.configs.template_config import SMSTemplateConfig, EmailTemplateConfig, \
    TelegramTemplateConfig
from notification_services.notification.factories.context_factory import EmailContextFactory, SMSContextFactory, \
    TelegramContextFactory
from notification_services.notification.service import EmailNotificationService, NotificationService, \
    SMSNotificationService, TelegramNotificationService


class NotificationRegistry:

    def __init__(self):
        self._services = {}
        self._register_default_services()

    def _register_default_services(self):
        self.register(
            NotificationDestination.EMAIL,
            EmailNotificationService(EmailContextFactory(), EmailTemplateConfig)
        )
        self.register(
            NotificationDestination.SMS,
            SMSNotificationService(SMSContextFactory(), SMSTemplateConfig)
        )
        self.register(
            NotificationDestination.TELEGRAM,
            TelegramNotificationService(TelegramContextFactory(), TelegramTemplateConfig)
        )


    def register(self, destination: NotificationDestination, service: NotificationService):
        self._services[destination] = service

    def get_service(self, destination: NotificationDestination) -> NotificationService:
        service = self._services.get(destination)
        if not service:
            raise ValueError(f"No service registered for destination: {destination}")
        return service
