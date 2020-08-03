from rest_framework.exceptions import APIException

class LoginRequiredError(APIException):
    
    status = None
    default_detail = None
