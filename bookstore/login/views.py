import jwt
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db import connection as conn
from .serializer import LoginSerializer, OTPSerializer
from rest_framework.response import Response
from .otp import send_otp, gen_otp
from .tasks import send_otp_to_user_while_login
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .services import (
    check_if_otp_generated_for_more_than_limit_for_user,
    check_if_user_is_blocked,
    login_required,
)
from bookstore.redis_setup import get_redis_instance
from bookstore import settings
from response_codes import get_response_code
from .default_jwt import jwt_encode
from bookstore.utility import DataBaseOperations as db
from login.services import get_current_user
from redis import DataError
from bookstore.book_store_exception import BookStoreError
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
from .models import LoginManager

# Create your views here.


class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        login_id = request.data["login_id"]
        password = request.data["password"]
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                cursor = conn.cursor()
                phone_no = LoginManager.get_user(login_id, password)
                if phone_no:
                    check_if_otp_generated_for_more_than_limit_for_user(phone_no)
                    check_if_user_is_blocked(phone_no)
                    random_otp = gen_otp()
                    send_otp_to_user_while_login.delay(phone_no, random_otp)
                    LoginManager.store_onto_OTP_table(phone_no, random_otp)
                    response = get_response_code("otp_sent")
                    response["Phone No."] = phone_no
                    return Response(response)
                else:
                    return Response(get_response_code("login_failed"))
            except TypeError:
                return Response(get_response_code("login_failed"))
            except Exception:
                return Response(get_response_code("generic_response"))
            finally:
                cursor.close()
        return Response(serializer.errors)


class VerifyOTPView(APIView):
    @swagger_auto_schema(request_body=OTPSerializer)
    def post(self, request):
        phone_no = request.headers.get("x_phoneno")
        otp = request.data["otp"]
        redis_instance = get_redis_instance()
        if not phone_no:
            raise BookStoreError(get_response_code("no_headers"))
        try:
            cursor = conn.cursor()
            original_otps = LoginManager.get_otp_for_phone_no(phone_no)

            if original_otps:
                latest_otp = original_otps[len(original_otps) - 1][0]
                latest_otp_send_time = original_otps[len(original_otps) - 1][1]
                elasped_time = (timezone.now() - latest_otp_send_time).total_seconds()
                if otp == latest_otp and int(elasped_time) < int(
                    settings.OTP_EXPIRY_TIME
                ):
                    user_id = LoginManager.get_user_id_from_phone_no(phone_no)
                    token = jwt_encode(user_id)
                    redis_instance.set(user_id, token)
                    LoginManager.delete_otp_for_authenticated_user(phone_no)
                    response = get_response_code("verify_response")
                    response["token"] = token
                    return Response(response)
                else:
                    return Response(get_response_code("otp_invalid"))
            else:
                return Response(get_response_code("otp_not_generated"))
        finally:
            cursor.close()


@api_view(("GET",))
@login_required
def logout(request):
    user_id = get_current_user(request)
    redis_instance = get_redis_instance()
    try:
        redis_instance.delete(user_id)
    except DataError:
        raise BookStoreError(get_response_code("login_required"))
    except Exception:
        return Response(get_response_code("generic_response"))
    return Response(get_response_code("logout"))
