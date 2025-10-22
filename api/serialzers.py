from rest_framework import serializers
from base.models import Restaurant, Rating, Sale

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('income', 'expenditure', 'profit_for_single_rest')

class AllRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('name', 'restaurant_type', 'avg_rates', 'opened_at')

class CustomRestaurantSerializer(serializers.ModelSerializer):
    sales = SalesSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Restaurant
        fields = ('name', 'username', 'restaurant_type', 'opened_at','avg_rates', 'sales')


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

