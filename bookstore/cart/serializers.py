from rest_framework import serializers


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    quantity_in_cart = serializers.CharField(max_length=255)
    quantity = serializers.CharField(max_length=255)
    price = serializers.CharField()
    description = serializers.CharField(max_length=255)
