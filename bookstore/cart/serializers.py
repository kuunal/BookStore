from rest_framework import serializers


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
