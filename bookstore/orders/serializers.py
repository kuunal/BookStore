from rest_framework import serializers 

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.IntegerField()
    user_id = serializers.IntegerField() 
    quantity = serializers.IntegerField()
    total = serializers.IntegerField()
    address = seriaizers.CharField(max_length=255)
    paid = serializers.IntegerField()
    is_delivered = serializers.IntegerField()