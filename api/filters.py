import django_filters
from base.models import Restaurant, Rating

class UserRestaurantFilter(django_filters.FilterSet):
    class Meta:
        model = Restaurant
        fields = {
            'name': ['icontains', 'contains'],
            # 'avg_rates': ['gt', 'lt', 'gte', 'lte'],
        }


class RatingsFilter(django_filters.FilterSet):
    class Meta:
        model = Rating
        fields = {
            "score": ['lt', 'gt', 'range', 'iexact'],
        }