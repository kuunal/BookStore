from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import WishListModel
from rest_framework.response import Response
from products.models import Product
from login.services import get_current_user
from rest_framework.decorators import api_view
from .serializer import ProductSerializer
from response_codes import get_response_code
from django.db import connection, IntegrityError
from login.services import login_required

class WishListView(APIView):

    @login_required
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
        
    @login_required
    def delete(self, request, id):
        user_id = get_current_user(request)
        result = WishListModel.objects.delete(id, user_id)
        if result == 0:
            return Response(get_response_code('wishlist_delete_does_exists'))
        return Response(get_response_code('deleted_wishlist_item'))


@api_view(('GET',))
@login_required
def add_to_wishlist(request):
    product_id = request.GET.get('id')
    if not product_id.isnumeric():
        return Response(get_response_code('invalid_product'))
    user_id  = get_current_user(request)
    try:
        cursor = connection.cursor()
        cursor.execute('select count(*) from wishlists where product_id = %s and user_id = %s', (product_id, user_id) )
        count = cursor.fetchone()
        count = count[0]
        if count > 0:
            return Response(get_response_code('product_already_in_wishlist'))
        wishlist = WishListModel(user_id=user_id, product_id=product_id)
        wishlist.save()
    except IntegrityError:
        return Response(get_response_code('invalid_product_id'))
    finally:
        cursor.close()
    return Response(get_response_code('added_to_wishlist'))