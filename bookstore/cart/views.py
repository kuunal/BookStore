from django.shortcuts import render
from rest_framework.views import APIView
from products.serializer import ProductSerializer
from products.models import Product
from rest_framework.response import Response
from django.db import connection, IntegrityError
from login.services import get_current_user
from .models import CartModel

class CartView(APIView):
    def get(self, request, id=None):
        user_id  = get_current_user(request)
        if id:
            try:
                cart_items = CartModel.objects.get(id, user_id)
                products = Product.objects.get(str(wishlist.product_id))
            except IndexError:
                return Response(get_response_code('invalid_product_id'))
        else:
            cart_items = CartModel.objects.all(params=user_id)
            products = Product.objects.filter(cart_items)
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)

