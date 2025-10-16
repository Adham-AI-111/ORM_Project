from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantListAPIView.as_view(), name='restaurant-list'),
    path('ratings/', views.RatingsListApiView.as_view(), name='ratings-list'),
    path('sales/', views.SalesListApiView.as_view(), name='sales-list'),
]
