from django.urls import path
from .views import ProductView

urlpatterns = [
    path('/', ProductView.as_view(), name="product_list"),
    path('/<str:pk>', ProductView.as_view(), name="product_list")
]
