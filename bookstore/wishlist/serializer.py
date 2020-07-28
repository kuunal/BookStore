from rest_framework import serializers
from products.serializer import ProductSerializer
from .models import WishListModel
from .services import get_current_user

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)  
    email = serializers.EmailField(max_length=100)
    phone_no = serializers.CharField(max_length=13)

class WishListSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def create(self, validated_data):
        wishlist_obj = WishListModel()
        wishlist_obj.user_id = get_current_user()
        wishlist_obj.product_id = validated_data['product_id']
        wishlist_obj.save()
        return wishlist_obj





