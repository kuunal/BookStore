from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection as conn

# Create your views here.

class LoginView(APIView):   


    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        cursor = conn.cursor()
        cursor.execute("""select count(*) from users where email = %s and password = %s """ % (email,password))
        count = cursor.fetchone()
        return Response(200) if count > 0 else Response(401)