from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializer import WishListSerializer
from .models import WishListModel
from rest_framework.response import Response
from products.models import Product
from login.services import get_current_user
from .serializer import ProductSerializer
from response_codes import get_response_code
from django.db import connection, IntegrityError

class WishListView(APIView):
    def get(self, request, id=None):
        user_id  = get_current_user(request)
        if id:
            try:
                wishlist = WishListModel.objects.get(id, user_id)
                products = Product.objects.get(str(wishlist.product_id))
            except IndexError:
                return Response(get_response_code('invalid_product_id'))
        else:
            wishlist = WishListModel.objects.all(params=user_id)
            products = Product.objects.filter(wishlist)
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)


    def post(self, request):
        product_id = request.data['product_id']
        user_id  = get_current_user(request)
        serializer = WishListSerializer(data=request.data)
        if serializer.is_valid():
            try:
                cursor = connection.cursor()
                cursor.execute('select count(*) from wishlists where product_id = %s and user_id = %s', (product_id, user_id) )
                count = cursor.fetchone()
                count = count[0]
                if count > 0:
                    return Response(get_response_code('product_already_in_wishlist'))
            except IntegrityError:
                return Response(get_response_code('invalid_product_id'))
            finally:
                cursor.close()
            serializer.save(user_id=user_id)
            return Response(get_response_code('added_to_wishlist'))
        return Response(get_response_code('invalid_product'))

        

    def delete(self, request, id):
        user_id = get_current_user(request)
        WishListModel.objects.delete(id, user_id)
        return Response(get_response_code('deleted_wishlist_item'))

