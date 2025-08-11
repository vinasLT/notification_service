import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import aiosmtplib
from config import settings
from schemas import EmailNotification


async def send_templated_email(data:EmailNotification):
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template(data.template_name)
    html_content = template.render(data.context.model_dump())

    msg = MIMEMultipart("alternative")
    msg['From'] = settings.SENDER_EMAIL
    msg['To'] = data.recipient
    msg['Subject'] = data.subject
    msg.attach(MIMEText(html_content, "html"))

    await aiosmtplib.send(
        msg,
        hostname=settings.SMPT_SERVER,
        port=settings.SMPT_PORT,
        start_tls=True,
        username=settings.SENDER_EMAIL,
        password=settings.EMAIL_PASSWORD,
    )


#
#
if __name__ == "__main__":
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "your_email@gmail.com"
    password = "your_password"
    sender = "your_email@gmail.com"
    recipient = settings.SENDER_EMAIL
    subject = "Письмо с шаблоном Jinja2"

    context = {
        "expire_minutes": "15",
        "code": "12345",
        "year": '2025',
        'company_name': 'VINAS',
        'link': 'https://www.google.com'
    }
    asyncio.run(send_templated_email(recipient, subject, "code_email.html", context))
#
