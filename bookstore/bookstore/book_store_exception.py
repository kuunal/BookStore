from rest_framework.exceptions import APIException

class BookStoreError(APIException):
    
    status = None
    default_detail = None
