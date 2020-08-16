from django.urls import path
from .views import CartView, add_to_cart, get_view, order

urlpatterns = [
    path('/', get_view,name="cart_items"),
    path('/upsert', add_to_cart, name="cart_upsert"),
    path('/<int:id>', CartView.as_view(), name="cart_detail"),
    path('/order', order, name="cart_order")
]
