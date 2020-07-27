import random
from twilio.rest import Client
from bookstore import settings
from django.db import connection as conn
from datetime import datetime
from django.utils import timezone

 
def send_otp(phone_no):

    characters_for_otp = '1234567890abcdefghijklmnopqrstuvwxyz'
    number_of_character_in_otp = 6
    random_otp = ""
    for characters in range(number_of_character_in_otp):
        random_otp+=random.choice(characters_for_otp)

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                        body = f'Your otp is {random_otp}',
                        from_= settings.TWILIO_NUMBER,
                        to=phone_no
                    )
    try:
        query = 'insert into otp_history values (%s, %s, %s)' % (phone_no, random_otp, timezone.now())
        cursor = conn.cursor()
    finally:
        cursor.close()

    return random_otp
