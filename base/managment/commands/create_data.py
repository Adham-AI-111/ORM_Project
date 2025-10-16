from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from base.models import Restaurant, Rating, Sale
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **kwargs):
        user = User.objects.get(username='testuser')
        if not user:
            user = User.objects.create_user(username='testuser', password='password')
        else:
            user = user

        # # Create sample restaurants
        restaurant_types = [choice[0] for choice in Restaurant.RestaurantType.choices]
        for i in range(13):
            restaurant, created = Restaurant.objects.get_or_create(
                name=f'Restaurant {i+1}',
                user=user,
                latitude=random.uniform(-90.0, 90.0),
                longitude=random.uniform(-180.0, 180.0),
                restaurant_type=random.choice(restaurant_types),
                opened_at=datetime.now().date() - timedelta(days=random.randint(1, 1000))
            )
            if created:
                print(f'Created {restaurant.name}')

        #     # Create sample ratings
        #     for j in range(13):
        #         rating, created = Rating.objects.get_or_create(
        #             restaurant=restaurant,
        #             user=user,
        #             score=random.randint(1, 5)
        #         )
        #         if created:
        #             print(f'Created rating {rating.score} for {restaurant.name}')

        #     # Create sample sales
        #     for k in range(30):
        #         sale, created = Sale.objects.get_or_create(
        #             restaurant=restaurant,
        #             income=random.uniform(100.0, 3000.0),
        #             date=datetime.now() - timedelta(days=random.randint(1, 200))
        #         )
        #         if created:
        #             print(f'Created sale of income {sale.income} for {restaurant.name}')

            # Create sample expenditure
            for k in range(30):
                sale, created = Sale.objects.get_or_create(
                    restaurant=restaurant,
                    expenditure=random.uniform(100.0, 2400.0),
                    date=datetime.now() - timedelta(days=random.randint(1, 200))
                )
                if created:
                    print(f'Created expenditure of expenditure {sale.expenditure} for {restaurant.name}')
        