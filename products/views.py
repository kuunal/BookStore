from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.respose import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.models import connection as conn
from serializers import ProductListSerializer as prod_serializer
from .models import Product

# Create your views here.
class BookListView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = prod_serializer(book_list, many=True)
        return Response(serializer.data)