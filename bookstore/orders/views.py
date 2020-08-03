from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrderSerializer, ResponseSerializer
from login.services import get_current_user
from rest_framework.response import Response
from response_codes import get_response_code
from .models import OrderModel
from login.tasks import order_placed_mail_to_user
from bookstore import settings

# Create your views here.
class OrderView(APIView):

    def get(self, request):
        user_id = get_current_user(request)
        orders = OrderModel.objects.filter(user_id)
        serializer = ResponseSerializer(orders, many=True)
        total = sum([total.price if total.quantity == 1 else total.price*total.quantity for total in orders])
        return Response({'order':serializer.data, 'total':total})
        
        

    def post(self, request):
        user_id = get_current_user(request)
        serializer = OrderSerializer(data=request.data)
        total = 0
        if serializer.is_valid():
            serializer.save(user_id=user_id)
            return Response(get_response_code('order_placed'))
        return Response(serializer.errors)

