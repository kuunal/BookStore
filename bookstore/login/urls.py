from django.urls import path
from .views import LoginView, VerifyOTPView


urlpatterns = [
    path('/', LoginView.as_view(), name="login"),
    path('/verify/', VerifyOTPViewas_view())
]
