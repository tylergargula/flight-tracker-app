from twilio.rest import Client
import os

twilio_sid = os.environ["TWILIO_SID"]
twilio_auth_token = os.environ["TWILIO_AUTH"]
twilio_phone_number = os.environ["TWILIO_PHONE"]
user_phone_number = os.environ["USER_PHONE"]


class NotificationManager:
    def __init__(self):
        self.client = Client(twilio_sid, twilio_auth_token)

    def send_sms(self, message, google_link):
        message = self.client.messages.create(
            body=f"{message}\n{google_link}",
            from_=twilio_phone_number,
            to=user_phone_number
        )
        print(f"SMS Message:\n{message.body}\n{message.sid}")