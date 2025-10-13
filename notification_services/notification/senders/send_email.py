import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader
import aiosmtplib
from config import settings
from notification_services.notification.schemas.email import EmailNotification, EmailContext, EmailCodeContext
from utils import BASE_DIR


async def send_templated_email(data:EmailNotification):
    env = Environment(loader=FileSystemLoader(BASE_DIR / 'src/templates'))
    template = env.get_template(data.template_name)
    html_content = template.render(data.context.model_dump())

    msg = MIMEMultipart("alternative")
    msg['From'] = settings.SENDER_EMAIL
    msg['To'] = data.recipient
    msg['Subject'] = data.subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMPT_SERVER,
            port=settings.SMPT_PORT,
            start_tls=True,
            username=settings.SENDER_EMAIL,
            password=settings.EMAIL_PASSWORD,
        )
        print("Email sent successfully")
    except Exception as e:
        print(f"Error while sending email: {e}")


if __name__ == "__main__":
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "your_email@gmail.com"
    password = "your_password"
    sender = "your_email@gmail.com"
    recipient = settings.SENDER_EMAIL
    subject = "Письмо с шаблоном Jinja2"


    context = EmailCodeContext(user_uuid='test-key', notification_uuid='test-key', code='123456', expire_minutes=10, year=2023)

    asyncio.run(send_templated_email(EmailNotification(recipient='peyrovskaaa@gmail.com', subject=subject, context=context, template_name='code_email.html')))
