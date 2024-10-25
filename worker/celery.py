import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from app.settings import settings

celery = Celery(__name__)

celery.conf.broker_url = settings.CELERY_REDIS_URL
celery.conf.result_backend = settings.CELERY_REDIS_URL


@celery.task(name='send_email')
def send_email_task(subject: str, text: str, to: str):
    msg = _build_message(subject, text, to)
    _send_mail(msg)


def _build_message(subject: str, text: str, to: str) -> MIMEMultipart:
    msg = MIMEMultipart()

    msg["From"] = settings.from_email
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(text, "plain"))
    return msg


def _send_mail(msg: MIMEMultipart):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context) as server:
        server.login(settings.from_email, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
