from rest_framework import serializers 
from django.db import connection as cn
from .models import OrderModel
from django.core.exceptions import ValidationError

class OrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    address = serializers.CharField(max_length=255)

    def create(self, validated_data):
        order = OrderModel(**validated_data)
        order.save()
        return order



class ResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    quantity = serializers.CharField(max_length=255)
    price = serializers.CharField()
    description = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    