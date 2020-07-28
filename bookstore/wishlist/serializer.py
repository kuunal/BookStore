from rest_framework import serializers
from products.serializer import ProductSerializer

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)  
    email = serializers.EmailField(max_length=100)
    phone_no = serializers.CharField(max_length=13)

class WishListSerializer(serializers.Serializer):
    user_id  = serializers.IntegerField()
    product_id = ProductSerializer(read_only=True)



