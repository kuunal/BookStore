from rest_framework.serializers import Serializer


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 100)  
    email = serializers.EmailField(max_lenth = 100)
    phone_no = serializers.CharField(max_length=13)




