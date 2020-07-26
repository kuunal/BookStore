from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection as conn
from .serializer import LoginSerializer
from rest_framework.response import Response
from .otp import send_otp

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
            phone_no = cursor.fetchone()
            if phone_no[0] > 0:
                try:
                    send_otp(phone_no[0])
                except Exception:
                    return Response(404)
                return Response(200)  
        return Response(401)