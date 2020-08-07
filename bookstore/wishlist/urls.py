from django.urls import path, include
from rest_framework import routers 
from .views import WishListView, add_to_wishlist, get_view


urlpatterns = [
    path('/', get_view),
    path('/add', add_to_wishlist),
    path('/<str:id>', WishListView.as_view()),
]

