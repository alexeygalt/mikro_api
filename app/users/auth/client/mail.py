from worker.celery import send_email_task


class MailClient:
    @staticmethod
    def send_welcome_email(to: str) -> None:
        return send_email_task.delay(subject="Welcome Email", text="Welcome to mikro", to=to)
