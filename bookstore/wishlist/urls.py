from django.urls import path, include
from rest_framework import routers 
from .views import WishListView


urlpatterns = [
    path('/', WishListView.as_view()),
    path('/<str:id>', WishListView.as_view()),
]

