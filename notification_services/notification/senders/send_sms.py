from twilio.rest.api.v2010.account.message import MessageInstance

from config import settings
from core.logger import logger
from twilio.rest import Client

from notification_services.notification.schemas.sms import SMSNotification

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def validate_phone(phone_number: str) -> str:
    if not phone_number:
        return phone_number

    if phone_number.startswith('+'):
        return phone_number
    else:
        return '+' + phone_number


def send_sms(sms_data: SMSNotification)-> MessageInstance | None:

    branded_message = f"{sms_data.message}\n\n— {settings.COMPANY_NAME}\n{settings.COMPANY_LINK}"

    phone_number = validate_phone(sms_data.recipient)

    logger.info('Sending sms notification', extra={
        'phone_number': phone_number,
        'message': branded_message
    })

    try:
        sms_message = client.messages.create(
            body=branded_message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        logger.debug('Sms notification sent', extra={
            'phone_number': phone_number,
            'message_sid': sms_message.sid
        })
        return sms_message

    except Exception as e:
        logger.error('Error sending sms notification', extra={
            'phone_number': phone_number,
            'message': branded_message,
            'error': str(e)
        })
        return None
