from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantListAPIView.as_view(), name='restaurant-list'),
    path('restaurants/<int:rest_id>/', views.SingleRestaurantAPIView.as_view(), name='single-restaurant'),
    path('ratings/', views.RatingsListApiView.as_view(), name='ratings-list'),
    path('sales/', views.SalesListApiView.as_view(), name='sales-list'),
]
