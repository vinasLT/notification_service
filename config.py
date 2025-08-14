from enum import Enum

from pydantic_settings import BaseSettings

from utils import BASE_DIR


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # Application
    APP_NAME: str = 'notification-service'
    COMPANY_NAME: str = 'Vinas'
    COMPANY_LINK: str = 'http://localhost'
    DEBUG: bool = True
    ROOT_PATH: str = ''
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    @property
    def enable_docs(self) -> bool:
        return self.ENVIRONMENT in [Environment.DEVELOPMENT]

    # database
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "test_db"
    DB_USER: str = "postgres"
    DB_PASS: str = "testpass"

    # rabbitmq
    RABBITMQ_URL: str = 'amqp://guest:guest@localhost:5672/'
    RABBITMQ_EXCHANGE_NAME: str = 'events'
    RABBITMQ_QUEUE_NAME: str = 'notifications'

    # twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str = '+16056362156'

    # Email
    SENDER_EMAIL: str = 'peyrovskaaa@gmail.com'
    SMPT_SERVER: str = 'smtp.gmail.com'
    SMPT_PORT: int = 587
    EMAIL_PASSWORD: str

    LOGO_URL: str = 'https://i.imgur.com/QNuAY7v.png'

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()