from rest_framework import serializers
from .models import CartModel
from bookstore.book_store_exception import BookStoreError
from response_codes import get_response_code

class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    quantity = serializers.CharField(max_length=255)
    price = serializers.CharField()
    description = serializers.CharField(max_length=255)


class CartOrderSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)

class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


    def validate(self, validated_data):
        for values in validated_data.values():
            if values <= 0:
                raise BookStoreError(get_response_code("invalid_data"))
        return validated_data


    def create(self, validated_data):
        cart_object = CartModel(**validated_data)
        cart_object.save() 
        return cart_object


    

