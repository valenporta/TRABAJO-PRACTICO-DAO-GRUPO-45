import smtplib
from email.mime.text import MIMEText
from ..core.config import MAILTRAP_HOST, MAILTRAP_PORT, MAILTRAP_USER, MAILTRAP_PASS

def send_mail(to_email: str, subject: str, body: str) -> bool:
    if not (MAILTRAP_HOST and MAILTRAP_USER and MAILTRAP_PASS):
        return False
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "no-reply@example.local"
    msg["To"] = to_email
    with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as s:
        s.login(MAILTRAP_USER, MAILTRAP_PASS)
        s.send_message(msg)
    return True
