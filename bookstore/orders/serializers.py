from rest_framework import serializers 
from django.db import connection as cn
from .models import OrderModel
from django.core.exceptions import ValidationError

class OrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField() 
    quantity = serializers.IntegerField()
    address = serializers.CharField(max_length=255)

    def create(self, validated_data):
        product_id = validated_data['product_id']
        ordered_quantity = validated_data['quantity']
        try:
            cursor = cn.cursor()
            cursor.execute('select quantity from product where id = %s', (product_id,))
            available_quantity = cursor.fetchone()[0]
            if  available_quantity == 0 :
                raise ValidationError("Product out of stock") 
            if available_quantity < ordered_quantity:
                raise ValidationError("Product out of stock for that quantity") 
            order = OrderModel(**validated_data)
            order.save()
            return order
        finally:
            cursor.close()