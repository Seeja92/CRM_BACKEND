from twilio.rest import Client
from django.conf import settings


def initiate_twilio_call(to_number):
    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )

    call = client.calls.create(
        to=to_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"
    )

    return call