from rest_framework.serializers import Serializer
from products.serializers import ProductSerializer

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 100)  
    email = serializers.EmailField(max_lenth = 100)
    phone_no = serializers.CharField(max_length=13)

class WishListSerializer(serializers.Serializer):
    user_id  = UserSerializer(read_only=True)
    product_id = ProductSerializer(read_only=True)
    


