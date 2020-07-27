from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection as conn
from .serializer import LoginSerializer
from rest_framework.response import Response
from .otp import send_otp
from .tasks import send_otp_to_user_while_login

# Create your views here.

class LoginView(APIView):   
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            cursor = conn.cursor()
            cursor.execute(f'select phone_no from users where email = %s and password = %s ' , (email,password))
            phone_no = cursor.fetchone()[0]
            phone_no = '+91'+phone_no
            print(phone_no)    
            if phone_no:
                try:
                    send_otp_to_user_while_login.delay(phone_no) 
                except Exception:
                    return Response(404)
                return Response(200)  
        return Response(401)