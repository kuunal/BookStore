from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializer import WishListSerializer
from .models import WishListModel
from rest_framework.response import Response
from products.models import Product
from products.serializer import ProductSerializer

class WishListView(APIView):
    serializer_class = WishListSerializer
    def get(self, request, id=None):
        wishlist = WishListModel.objects.all() 
        if id:
            try:
                products = Product.objects.get(str(wishlist[int(id)].product_id))
            except IndexError:
                return Response({'status':'400', 'message':'No such product'})
        else:
            products = Product.objects.filter(wishlist)
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)
        