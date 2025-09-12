from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Restaurant(models.Model):
    class RestaurantType(models.TextChoices):
        FAST_FOOD = 'FF', 'Fast Food'
        ITALIAN = 'IT', 'Italian'
        EGYPTION = 'EG', 'Egyption'
        DRINKS = 'DR', 'Drinks'
        ARABIAN = 'AR', 'Arabian'
        OTHER = 'OT', 'Other'
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    website = models.URLField(blank=True, null=True)
    latitude = models.FloatField(default=0.0, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(default=0.0, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    restaurant_type = models.CharField(max_length=2, choices=RestaurantType.choices)
    opened_at = models.DateField()
    def __str__(self):
        return self.name
    
    def total_sales_amount(self):
        # using aggregate to sum up the amounts of all related sales
        return self.sales.aggregate(total=models.Sum('amount'))['total'] or 0.0


class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.restaurant.name} - {self.score} by {self.user.username}"


class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='sales')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
