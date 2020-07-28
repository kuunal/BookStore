from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import WishListSerializer
from .models import WishListModel
from rest_framework.response import Response

# Create your views here.
class WishListView(APIView):
    serializer_class = WishListSerializer
    def get(self, request):
        wishlist = WishListModel.objects.all() 
        serializer = WishListSerializer(data = wishlist)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(400)
