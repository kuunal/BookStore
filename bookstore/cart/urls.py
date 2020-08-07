from django.urls import path
from .views import CartView, add_to_cart, get_view, order

urlpatterns = [
    path('/', get_view),
    path('/upsert', add_to_cart),
    path('/<int:id>', CartView.as_view()),
    path('/order', order)
]
