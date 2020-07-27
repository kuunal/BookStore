from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection as conn
from .serializer import LoginSerializer
from rest_framework.response import Response
from .otp import send_otp, gen_otp
from .tasks import send_otp_to_user_while_login
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .services import check_if_otp_generated_for_more_than_limit_for_user, check_if_user_is_blocked
from bookstore.redis_setup import get_redis_instance

# Create your views here.

class LoginView(APIView):   
    serializer_class = LoginSerializer
    redis_instance  = get_redis_instance()

    def post(self, request):
        login_id = request.data['login_id']
        password = request.data['password']
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            try:
                cursor = conn.cursor()
                cursor.execute("select phone_no from users where (email = %s or phone_no like %s) and password = %s ", (login_id, '%'+login_id, password))
                phone_no = cursor.fetchone()
                phone_no = phone_no[0]
                if phone_no:
                    try:
                        check_if_otp_generated_for_more_than_limit_for_user(phone_no)
                        check_if_user_is_blocked(phone_no)
                    except ValidationError as e:
                        return Response({'status':400,'message':str(e)})
                    random_otp = gen_otp()
                    send_otp_to_user_while_login.delay(phone_no, random_otp) 
                    cursor.execute('insert into otp_history(phone_no, otp, datetime) values(%s, %s, %s)',(phone_no, random_otp, timezone.now()))
                    LoginView.redis_instance.set(phone_no, random_otp)
                    return Response(200)
            except Exception as e:
                return Response(str(e))
            finally:
                cursor.close()
        return Response(401)
