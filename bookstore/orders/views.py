from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrderSerializer
from login.services import get_current_user
from rest_framework.response import Response

# Create your views here.
class OrderView(APIView):

    def post(self, request):
        user_id = get_current_user(request)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
            return Response(200)
        return Response(serializer.errors)

