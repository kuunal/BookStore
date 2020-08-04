import re
from rest_framework import serializers
from django.core.exceptions import ValidationError
from response_codes import get_response_code
from bookstore.book_store_exception import BookStoreError

class LoginSerializer(serializers.Serializer):
    login_id = serializers.CharField(max_length=199)
    password = serializers.CharField(max_length=100)
    


    def validate_login_id(self, value):
        if re.match("^[a-zA-Z0-9]+[\\.\\-\\+\\_]?[a-zA-Z0-9]+@[a-zA-Z0-9]+[.]?[a-zA-Z]{2,4}[\\.]?([a-z]{2,4})?$", value) or re.match("[0-9]{10}", value):
            return value
        raise BookStoreError(get_response_code('invalid_login'))