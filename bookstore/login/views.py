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
                    return Response({'status':200, 'message':'Please verify by entering OTP sent to you'})
            except Exception as e:
                return Response(e)
            finally:
                cursor.close()
        return Response(401)



class VerifyOTPView(APIView):
    def post(self, request):
        phone_no = request.headers.get('x_phoneno')
        otp = request.data['otp']
        redis_instance  = get_redis_instance()
        cursor = conn.cursor()
        cursor.execute('select otp, datetime from otp_history where phone_no = %s', [phone_no])
        original_otps = cursor.fetchall() 
        if otp:
            latest_otp = original_otps[len(original_otps)-1][0]
            latest_otp_send_time  = original_otps[len(original_otps)-1][1]
            elasped_time = (timezone.now()-latest_otp_send_time).total_seconds()
            
            if otp == latest_otp and elasped_time < 300 :
                # redis_instance.set(otp[:-1][1], otp)
                cursor.execute('delete from otp_history where phone_no = %s', [phone_no])
                return Response(200)
            else:
                return Response({'status':401,'message':'OTP is expired'})
        else:
            return Response({'status':401,'message':'Invalid OTP'})
        
