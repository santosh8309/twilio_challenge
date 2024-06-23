# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

from dotenv import load_dotenv


def send_whatsapp_sms(msg, to_phone):

    load_dotenv()
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=msg,
        from_=str("whatsapp:" + os.environ.get("FROM_PHONE")),
        to=str("whatsapp:" + to_phone),
    )

    print(message.sid)
