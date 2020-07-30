from rest_framework import serializers
from products.serializer import ProductSerializer
from .models import WishListModel
from login.services import get_current_user

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)  
    email = serializers.EmailField(max_length=100)
    phone_no = serializers.CharField(max_length=13)

class WishListSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def create(self, validated_data):
        wishlist_obj = WishListModel(**validated_data)
        wishlist_obj.save()
        return wishlist_obj 


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    description = serializers.CharField(max_length=255)
    




