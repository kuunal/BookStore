import random
from twilio.rest import Client

def send_otp(phone_no):

    characters_for_otp = '1234567890abcdefghijklmnopqrstuvwxyz'
    number_of_character_in_otp = 6
    random_otp = ""

    for characters in range(number_of_character_in_otp):
        random_otp+=random.choice(characters_for_otp)

    account_sid = 'AC24101a599eeb4552cb56f52fd8c06619'
    auth_token = '27265addf7e0077bbb7b58c86b000faf'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                        body = f'Your otp is {random_otp}',
                        from_='+17372147866',
                        to='phone_no'
                    )


    return random_otp
