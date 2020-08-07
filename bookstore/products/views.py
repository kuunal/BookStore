import pickle
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
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from bookstore.redis_setup import get_redis_instance
from .services import get_cache_item, set_cache

page_param = openapi.Parameter('pageno', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_INTEGER)
sortby_param = openapi.Parameter('sortby', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)
desc_param = openapi.Parameter('des', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)


class ProductView(APIView):

    @swagger_auto_schema(manual_parameters=[page_param, sortby_param, desc_param], )
    def get(self, request, pk=None):
        if pk:
            pk = pk.lower()
            products = Product.objects.get(pk)
        else:
            redis_instance = get_redis_instance()
            products = get_cache_item()
            if not products:
                products = Product.objects.all()
                set_cache(products)
            try:
                sort_by = 'id' if not request.GET.get('sortby') else request.GET.get('sortby').lower()
                sort_type = True if request.GET.get('des') == 'true' else False
                products.sort(key= lambda obj: getattr(obj, sort_by), reverse=sort_type)    
            except AttributeError:
                sort_by = 'author'
        paginator_object = Paginator(products,PAGINATOR_PAGE_LIMIT)
        page_no = 1 if request.GET.get('pageno') == None else request.GET.get('pageno')
        try:
            product_obj = paginator_object.page(page_no)
        except EmptyPage:
            product_obj = paginator_object.page(1)
        serializer = prod_serializer(product_obj, many=True)
        response = serializer.data
        return Response(response) if response else Response (get_response_code('invalid_product_id'))
