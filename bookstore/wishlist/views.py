from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import WishListModel
from rest_framework.response import Response
from products.models import Product
from login.services import get_current_user
from rest_framework.decorators import api_view
from .serializer import ProductSerializer, WishListSerializer
from response_codes import get_response_code
from django.db import connection, IntegrityError
from login.services import login_required
from bookstore.utility import DataBaseOperations as db
from bookstore.book_store_exception import BookStoreError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class WishListView(APIView):

    '''
        Detail view ow wishlist item
    '''
    @login_required
    def get(self, request, id=None):
        user_id  = get_current_user(request)
        if id:
            try:
                wishlist = WishListModel.objects.get(id, user_id)
                products = Product.objects.get(str(wishlist.product_id))
            except IndexError:
                raise BookStoreError(get_response_code('invalid_product_id'))
        else:
            wishlist = WishListModel.objects.all(params=user_id)
            products = Product.objects.filter(wishlist)
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)
        
    @login_required
    def delete(self, request, id):
        user_id = get_current_user(request)
        result = WishListModel.objects.delete(id, user_id)
        if result == 0:
            return Response(get_response_code('wishlist_delete_does_exists'))
        return Response(get_response_code('deleted_wishlist_item'))


'''
    Add onto wishlist of logged in user
'''
@swagger_auto_schema(method='post', request_body=WishListSerializer)
@api_view(('POST',))
@login_required
def add_to_wishlist(request):
    serializer = WishListSerializer(data=request.data)
    if serializer.is_valid():
        user_id  = get_current_user(request)
        serializer.save(user_id= user_id)
        return Response(get_response_code('added_to_wishlist'))
    return Response(serializer.errors)
    

'''
    Get all wishlist items for logged in user
'''
@api_view(('GET',))
@login_required
def get_view(request):
    user_id = get_current_user(request)
    wishlist = WishListModel.objects.all(params=user_id)
    products = Product.objects.filter(wishlist)
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)