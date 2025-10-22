from django.urls import path
from . import views

urlpatterns = [
    path('my-restaurants/', views.UserRestaurantListCreateAPIView.as_view()),
    path('my-restaurants/<int:rest_id>/', views.SingleRestaurantAPIView.as_view()),
    path('all-restaurants/', views.AllRestaurantListAPIView.as_view()),
    path('ratings/', views.RatingsListApiView.as_view()),
    path('sales/', views.SalesListApiView.as_view()),
]
