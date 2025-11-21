# flaskr/notifications/sms_sender.py

from twilio.rest import Client
from flask import current_app

def send_sms(to_number, message):
    """Send SMS using Twilio."""
    account_sid = current_app.config.get("TWILIO_ACCOUNT_SID")
    auth_token = current_app.config.get("TWILIO_AUTH_TOKEN")
    from_number = current_app.config.get("TWILIO_PHONE_NUMBER")

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        current_app.logger.info(f"SMS sent to {to_number}")

    except Exception as e:
        current_app.logger.error(f"SMS failed to {to_number}: {e}")
        raise e
