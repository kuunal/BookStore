from rest_framework import serializers
from products.serializer import ProductSerializer
from .models import WishListModel
from login.services import get_current_user

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    description = serializers.CharField(max_length=255)
    




