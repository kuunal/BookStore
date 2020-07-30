import jwt
from rest_framework import authentication, exceptions
from bookstore import settings
from datetime import timedelta
from django.utils import timezone



def jwt_decode(token):
    if not token:
        raise exceptions.AuthenticationFailed("Your token is invalid")  
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY)
        user_email=payload.get('user_id')
        return user_email
    except jwt.DecodeError as identifier:   
        raise exceptions.AuthenticationFailed("Your token is invalid")
    except jwt.ExpiredSignatureError as indentifier:
        raise exceptions.AuthenticationFailed("your token is expired!")   

def jwt_encode(user_id):
    return jwt.encode({'user_id':user_id,
                    'exp': timezone.now() + timedelta(seconds=int(settings.JWT_EXPIRATION_TIME)),
                    },settings.JWT_SECRET_KEY)
