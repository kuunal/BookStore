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
from .serializers import CartSerializer
from orders.services import get_latest_order_id
from orders.models import OrderManager
from login.services import login_required

class CartView(APIView):
    
    @login_required
    def get(self, request, id=None):
        user_id  = get_current_user(request)
        if id:
            try:
                result = CartModel.objects.get(id, user_id)
            except IndexError:
                return Response(get_response_code('invalid_product_id'))
        else:
            result = CartModel.objects.all(user_id)
        total = sum([total.price if total.quantity == 1 else total.price*total.quantity for total in result])
        serializer = CartSerializer(result, many = True)
        return Response({'cart':serializer.data, 'total':total})

    @login_required
    def delete(self, request, id):
        user_id = get_current_user(request)
        result = CartModel.objects.delete(id, user_id)
        if result == 0:
            return Response(get_response_code('item_not_in_cart'))
        return Response(get_response_code('removed_cart_item'))

    @login_required
    def post(self, request, id=None):
        user_id = get_current_user(request)
        address = request.data['address']
        if id:
            result = CartModel.objects.get(id,user_id)
        else:
            result = CartModel.objects.all(user_id)
        total = sum([total.price if total.quantity == 1 else total.price*total.quantity for total in result])
        id = get_latest_order_id()
        OrderManager.insert(result, total, address, id)
        return Response(200)

@api_view(('GET',))
@login_required
def add_to_cart(request):
    product_id = request.GET.get('id')
    quantity = 1 if request.GET.get('quantity') == None else request.GET.get('quantity')
    if not product_id.isnumeric() and not quantity.isnumeric() and product_id !=0 and quantity!=0:
        return Response(get_response_code('invalid_product'))
    user_id  = get_current_user(request)
    try:
        cart_item = CartModel(user_id=user_id, product_id=product_id, quantity=quantity)
        result = cart_item.save()
        return Response(result)
    except ValidationError:
        return Response(get_response_code('out_of_stock'))
    except IntegrityError:
        return Response(get_response_code('invalid_product_id'))
    return Response(get_response_code('added_to_wishlist'))