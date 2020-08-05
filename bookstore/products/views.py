from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.db import connection as conn
from .serializer import ProductSerializer as prod_serializer
from .models import Product
from response_codes import get_response_code, PAGINATOR_PAGE_LIMIT
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
class ProductView(APIView):


    def get(self, request, pk=None):
        if pk:
            pk = pk.lower()
            products = Product.objects.get(pk)
        else:
            products = Product.objects.all()
            try:
                sort_by = id if not request.GET.get('sortby') else request.GET.get('sortby').lower()
                sort_type = True if request.GET.get('des') == 'true' else False
                products.sort(key= lambda obj: getattr(obj, sort_by), reverse=sort_type)    
            except AttributeError:
                sort_by = 'author'
            p = Paginator(products,PAGINATOR_PAGE_LIMIT)
            page_no = 1 if request.GET.get('pageno') == None else request.GET.get('pageno')
        try:
            p = p.page(page_no)
        except EmptyPage:
            p = p.page(1)
        serializer = prod_serializer(p, many=True)
        response = serializer.data
        return Response(response) if response else Response (get_response_code('invalid_product_id'))
