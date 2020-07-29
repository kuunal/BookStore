from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializer import WishListSerializer
from .models import WishListModel
from rest_framework.response import Response
from products.models import Product
from .services import get_current_user
from .serializer import ProductSerializer
from response_codes import responses
class WishListView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                wishlist = WishListModel.objects.get(id)
                products = Product.objects.get(str(wishlist.product_id))
            except IndexError:
                return Response(responses['index_error_wishlist'])
        else:
            wishlist = WishListModel.objects.all()
            products = Product.objects.filter(wishlist)
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)


    def post(self, request):
        product_id = request.data['product_id']
        serializer = WishListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(responses['added_to_wishlist'])
        return Response(responses['invalid_product'])

        

    def delete(self, request, id):
        WishListModel.objects.delete(id)
        return Response(responses['deleted_wishlist_item'])

