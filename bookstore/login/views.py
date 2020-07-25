from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection as conn
from .serializer import LoginSerializer
from rest_framework.response import Response

# Create your views here.

class LoginView(APIView):   
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            cursor = conn.cursor()
            cursor.execute(f'select count(*) from users where email = %s and password = %s ' , (email,password))
            count = cursor.fetchone()
            print(count)
            if count[0] > 0:
                return Response(200)  
        return Response(401)