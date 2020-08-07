from django.urls import path
from .views import CartView, add_to_cart, get_view

urlpatterns = [
    path('/', get_view),
    path('/add', add_to_cart),
    path('/<int:id>', CartView.as_view()),

]
