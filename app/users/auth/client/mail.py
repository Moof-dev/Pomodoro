
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.settings import Setting
from worker.celery import send_email_task


class MailClient:
    @staticmethod
    def send_welcome_email(to: str) -> None:
        #pass
        task_id = send_email_task.delay(subject="Test subject welcome pomodoro", text="Test subject welcome pomodoro",to=to)
        return task_id
