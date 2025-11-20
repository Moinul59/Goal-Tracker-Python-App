# flaskr/notifications/emailer.py

import smtplib
from email.mime.text import MIMEText
from flask import current_app

def send_email(to_email, subject, body):
    """Send email using SMTP (Gmail or any SMTP server)."""

    smtp_server = current_app.config.get("SMTP_SERVER")
    smtp_port = current_app.config.get("SMTP_PORT")
    smtp_user = current_app.config.get("SMTP_USERNAME")
    smtp_pass = current_app.config.get("SMTP_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [to_email], msg.as_string())
        current_app.logger.info(f"Email sent to {to_email}")

    except Exception as e:
        current_app.logger.error(f"Email failed to {to_email}: {e}")
        raise e
