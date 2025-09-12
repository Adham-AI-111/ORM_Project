from base.models import Restaurant, Rating, Sale
from django.contrib.auth.models import User

def run():
    user = User.objects.first()
    restaurant = Restaurant.objects.first()
    sale = Sale()
    sale.restaurant = restaurant
    sale.amount = 8000
    sale.date = "2023-10-11"
    sale.save()

    # ?=======================
    # restaurant = Restaurant()
    # restaurant.name = "Egyption Food"
    # restaurant.user = user
    # restaurant.latitude = 30.0444
    # restaurant.longitude = 31.2357
    # restaurant.restaurant_type = Restaurant.RestaurantType.EGYPTION
    # restaurant.opened_at="2023-01-01"  # ✅ correct format
    # restaurant.save()
    # ?=======================
    # rating = Rating()
    # rating.restaurant = restaurant
    # rating.user = user
    # rating.score = 4
    # rating.save()
    print("Script is running")