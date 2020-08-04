import jwt
from rest_framework import authentication, exceptions
from bookstore import settings
from datetime import timedelta
from django.utils import timezone
from bookstore.book_store_exception import BookStoreError
from response_codes import get_response_code

def jwt_decode(token):
    print(settings.JWT_SECRET_KEY)
    if not token:
        raise BookStoreError(get_response_code('login_required'))  
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY)
        user_email=payload.get('user_id')
        return user_email
    except jwt.DecodeError as identifier:   
        raise BookStoreError(get_response_code('jwt_decode_error'))
    except jwt.ExpiredSignatureError as indentifier:
        raise BookStoreError(get_response_code('jwt_signature_expired'))   

def jwt_encode(user_id):
    return jwt.encode({'user_id':user_id,
                    'exp': timezone.now() + timedelta(seconds=settings.JWT_EXPIRATION_TIME),
                    },settings.JWT_SECRET_KEY)
