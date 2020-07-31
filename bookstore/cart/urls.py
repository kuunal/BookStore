from django.urls import path
from .views import CartView, add_to_cart

urlpatterns = [
    path('/', CartView.as_view()),
    path('/add', add_to_cart),
    path('/<int:id>', CartView.as_view()),

]
