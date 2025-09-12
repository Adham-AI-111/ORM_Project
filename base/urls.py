from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('add-restaurant/', views.add_restaurant, name='add_restaurant'),
    path('edit-restaurant/<int:restaurant_id>/', views.edit_restaurant, name='edit_restaurant'),
    path('delete-restaurant/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),
    path('rate-restuarant/', views.display_restaurants_to_rate, name='rate_restuarant'),
    path('rate-restuarant/<int:restaurant_id>/', views.rate_restaurant, name='rate_single_restuarant'),
    path('view-restaurant-sale/', views.restaurant_sale, name='view_restaurant_sale'),
    path('add-sales/<int:restaurant_id>/', views.add_sales, name='add_sales'),
]
