import random
from twilio.rest import Client
from bookstore import settings
from django.db import connection as conn
from datetime import datetime
from django.utils import timezone
from response_codes import TOTAL_NUMBER_OF_OTP_CHARACTER


def gen_otp():
    characters_for_otp = '1234567890abcdefghijklmnopqrstuvwxyz'
    number_of_character_in_otp = TOTAL_NUMBER_OF_OTP_CHARACTER
    random_otp = ""
    for characters in range(number_of_character_in_otp):
        random_otp+=random.choice(characters_for_otp)
    return random_otp

 
def send_otp(phone_no, random_otp):

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                        body = f'Your otp is {random_otp}',
                        from_= settings.TWILIO_NUMBER,
                        to=phone_no
                    )

    return random_otp
