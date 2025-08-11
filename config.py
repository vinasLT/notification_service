from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = 'notification-service'
    COMPANY_NAME: str = 'Vinas'
    DOMAIN: str = 'localhost'
    DEBUG: bool = True

    # database
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "test_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "testpass"

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