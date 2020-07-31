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

class CartView(APIView):
    def get(self, request, id=None):
        user_id  = get_current_user(request)
        if id:
            try:
                cart_items = CartModel.objects.get(id, user_id)
                products = Product.objects.get(str(cart_items.product_id))
            except IndexError:
                return Response(get_response_code('invalid_product_id'))
        else:
            cart_items = CartModel.objects.all(params=user_id)
            products = Product.objects.filter(cart_items)
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)

    def delete(self, request, id):
        user_id = get_current_user(request)
        result = CartModel.objects.delete(id, user_id)
        if result == 0:
            return Response(get_response_code('wishlist_delete_does_exists'))
        return Response(get_response_code('deleted_wishlist_item'))

@api_view(('GET',))
def add_to_cart(request):
    product_id = request.GET.get('id')
    if not product_id.isnumeric():
        return Response(get_response_code('invalid_product'))
    user_id  = get_current_user(request)
    try:
        cursor = connection.cursor()
        cursor.execute('select count(*) from cart where product_id = %s and user_id = %s', (product_id, user_id) )
        count = cursor.fetchone()
        count = count[0]
        if count > 0:
            return Response(get_response_code('product_already_in_wishlist'))
        cart_item = CartModel(user_id=user_id, product_id=product_id)
        cart_item.save()
    except IntegrityError:
        return Response(get_response_code('invalid_product_id'))
    finally:
        cursor.close()
    return Response(get_response_code('added_to_wishlist'))