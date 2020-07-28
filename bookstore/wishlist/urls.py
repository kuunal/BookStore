from django.urls import path, include
from rest_framework import routers 
from .views import WishListView

# wishlist_router = routers.DefaultRouter()
# wishlist_router.register('', WishListView)

urlpatterns = [
    # path('/', include(wishlist_router.urls))
    path('/', WishListView.as_view())
]

