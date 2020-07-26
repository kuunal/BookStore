import random
from twilio.rest import Client
from bookstore import settings

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
                        to='phone_no'
                    )


    return random_otp
