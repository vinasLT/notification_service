from enum import Enum

from pydantic_settings import BaseSettings

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # Application
    APP_NAME: str = 'notification-service'
    COMPANY_NAME: str = 'Vinas'
    COMPANY_LINK: str = 'localhost'
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

    RABBITMQ_URL: str = 'amqp://guest:guest@localhost:5672/'
    RABBITMQ_EXCHANGE_NAME: str = 'events'
    RABBITMQ_QUEUE_NAME: str = 'notifications'

    # Email
    SENDER_EMAIL: str = 'peyrovskaaa@gmail.com'
    SMPT_SERVER: str = 'smtp.gmail.com'
    SMPT_PORT: int = 587
    EMAIL_PASSWORD: str = 'gdop doko bapm pebm'

    LOGO_URL: str = 'https://i.imgur.com/QNuAY7v.png'


settings = Settings()