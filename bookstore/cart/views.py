from django.shortcuts import render
from rest_framework.views import APIView
from products.serializer import ProductSerializer
from products.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection, IntegrityError
from login.services import get_current_user
from .models import CartModel
from response_codes import get_response_code
from django.core.exceptions import ValidationError
from .serializers import CartSerializer, CartOrderSerializer, CartAddSerializer
from orders.services import get_latest_order_id
from orders.models import OrderManager
from login.services import login_required
from bookstore.book_store_exception import BookStoreError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CartView(APIView):
    
    '''
        Detailed view for cart product along with total based on quantity related to specific user 
    '''
    @login_required
    def get(self, request, id=None):
        user_id  = get_current_user(request)
        if id:
            try:
                result = CartModel.objects.get(id, user_id)
            except IndexError:
                return Response(get_response_code('invalid_product_id'))
        total = sum([total.price if total.quantity == 1 else total.price*total.quantity for total in result])
        serializer = CartSerializer(result, many = True)
        return Response({'cart':serializer.data, 'total':total})

    '''
        Delete product from cart if exists
    '''
    @login_required
    def delete(self, request, id=None):
        user_id = get_current_user(request)
        result = CartModel.objects.delete(id, user_id)
        if result == 0:
            return Response(get_response_code('item_not_in_cart'))
        return Response(get_response_code('removed_cart_item'))


'''
    Adding products into cart 
'''
@swagger_auto_schema(method='post', request_body=CartAddSerializer)
@api_view(('POST',))
@login_required
def add_to_cart(request):
    serializer = CartAddSerializer(data= request.data)
    if serializer.is_valid():
        user_id  = get_current_user(request)
        serializer.save(user_id=user_id)
        return Response(get_response_code('added_to_wishlist'))
    return Response(serializer.data)

'''
    Get all products from cart
'''
@api_view(('GET',))
@login_required
def get_view(request):
    user_id  = get_current_user(request)
    items = CartModel.objects.all(user_id)
    total = sum([item.price if item.quantity == 1 else item.price*item.quantity for item in items])
    serializer = CartSerializer(items, many = True)
    return Response({'cart':serializer.data, 'total':total})

'''
    Order all products from cart
'''
@swagger_auto_schema(method='post', request_body=CartOrderSerializer)
@api_view(('POST',))
@login_required
def order(request):
    user_id = get_current_user(request)
    address = request.data['address']
    items = CartModel.objects.all(user_id)
    if len(items) < 1:
        raise BookStoreError(get_response_code("no_product_to_order"))
    total = sum([item.price if item.quantity == 1 else item.price*item.quantity for item in result])
    if len(result)==0:
        raise BookStoreError(get_response_code('item_not_in_cart'))
    id = get_latest_order_id()
    OrderManager.insert(items, total, address, id)
    return Response(get_response_code('order_placed'))
