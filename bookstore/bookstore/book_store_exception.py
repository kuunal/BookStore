from rest_framework.exceptions import APIException


class BookStoreError(APIException):
    def __init__(self, res):
        self.status_code = res["status"]
        self.detail = res["message"]


from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code

    return response
