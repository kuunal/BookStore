from rest_framework import serializers
from products.serializer import ProductSerializer
from .models import WishListModel
from login.services import get_current_user
from bookstore.book_store_exception import BookStoreError
from response_codes import get_response_code    
from bookstore.utility import DataBaseOperations as db

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    description = serializers.CharField(max_length=255)

class WishListSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate(self, validated_data):
        for data in validated_data.values():
            if data <= 0:
                raise BookStoreError(get_response_code('invalid_data')) 
        return validated_data

    def create(self, validated_data):
        count = db.execute_sql('select count(*) from wishlists where product_id = %s and user_id = %s', (validated_data['product_id'], validated_data['user_id']), False)
        if count > 0:
            raise BookStoreError(get_response_code('product_already_in_wishlist'))
        wishlist_item = WishListModel(**validated_data)
        wishlist_item.save()
        return wishlist_item
    




