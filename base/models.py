from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, F, Sum

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
    
    @property
    def avg_rates(self):
        return self.ratings.aggregate(average=Avg('score'))['average'] or 0.0

    @property
    def total_sales_income(self):
        # using aggregate to sum up the amounts of all related sales
        return self.sales.aggregate(total=Sum('income'))['total'] or 0.0

    @property
    def total_sales_profit(self):
        # using aggregate to sum up the amounts of all related sales
        return self.sales.aggregate(total=Sum('profit'))['total'] or 0.0


class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.restaurant.name} - {self.score} by {self.user.username}"


class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='sales')
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expenditure = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateTimeField()

    @classmethod
    def total_income_for_rest(self):
        return Sale.objects.aggregate(total=Sum('income'))['total'] or 0.0
    
    @classmethod
    def total_profit_for_rest(self, restaurant_id):
        return self.objects.filter(restaurant__id=restaurant_id).aggregate(total=Sum('profit'))['total'] or 0.0
    
    @property
    def profit(self):
        # if the profit got by annotate will not appear on the serializer as a col, should be with this direct way
        return self.income - self.expenditure
 