from rest_framework import serializers
from base.models import Restaurant, Rating, Sale

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('income', 'expenditure', 'profit')

class RestaurantSerializer(serializers.ModelSerializer):
    sales = SalesSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ('name', 'user', 'restaurant_type', 'opened_at', 'sales')


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

