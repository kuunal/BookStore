from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=199)
    password = serializers.CharField(max_length=100)
