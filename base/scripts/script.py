from base.models import Restaurant, Rating, Sale
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random

def run():
    user = User.objects.all()[1]
    # restaurant = Restaurant.objects.first()
    # print(user)

    print(Rating.objects.all().count())

    # ?=======================
    # test the prefetch_related optimization
    restaurants = Restaurant.objects.prefetch_related('sales', 'ratings').all()
    ratings = restaurants.values('ratings__id', 'ratings__score', 'ratings__restaurant__name', 'ratings__user__username')
    print(restaurants.filter(sales__total_amount__gt=50000).distinct().count())
    # ?=======================
    # restaurant = Restaurant()
    # restaurant.name = "Pizza House"
    # restaurant.user = user
    # restaurant.latitude = 33.0444
    # restaurant.longitude = 65.2357
    # restaurant.restaurant_type = Restaurant.RestaurantType.FAST_FOOD
    # restaurant.opened_at="2024-06-01"  # ✅ correct format
    # restaurant.save()
    # ?=======================
    # rating = Rating()
    # rating.restaurant = restaurant
    # rating.user = user
    # rating.score = 4
    # rating.save()
    # ?======================
    # sale = Sale()
    # sale.restaurant = restaurant
    # sale.amount = 8000
    # sale.date = "2023-10-11"
    # sale.save()

    print("Script is running")