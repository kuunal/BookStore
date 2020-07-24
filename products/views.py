from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.respose import Response
from rest_framework.generics import ListAPIView
from django.models import connection as conn
from serializers import ProductListSerializer as prod_serializer

# Create your views here.
class BookListView(ListAPIView):

    def get_queryset(self):
        cursor = conn.cursor()
        book_list = cursor.execute("select * from product")
        serializer = prod_serializer(book_list)
        return serializer.data