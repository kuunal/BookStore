from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.db import connection as conn
from .serializer import ProductSerializer as prod_serializer
from .models import Product
from response_codes import get_response_code

# Create your views here.
class ProductView(APIView):


    def get(self, request, pk=None):
        if pk:
            pk = pk.lower()
            products = Product.objects.get(pk)
        else:
            sort_by = id if not request.GET.get('sortby') else request.GET.get('sortby')
            sort_type = True if request.GET.get('des') == 'true' else False
            products = Product.objects.all()
            try:
                products.sort(key= lambda obj: getattr(obj, sort_by), reverse=sort_type)    
            except AttributeError:
                sort_by = 'author'
        serializer = prod_serializer(products, many=True)
        response = serializer.data
        return Response(response) if response else Response (get_response_code('invalid_product_id'))
