from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializer import WishListSerializer
from .models import WishListModel
from rest_framework.response import Response
from products.models import Product
from .services import get_current_user
from products.serializer import ProductSerializer

class WishListView(APIView):
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


    def post(self, request):
        product_id = request.data['product_id']
        serializer = WishListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':200, 'message':'Added to wishlist'})
        return Response({'status':400, 'message':'invalid product'})

        