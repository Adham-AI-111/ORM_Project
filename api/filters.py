import django_filters
from base.models import Restaurant

class UserRestaurantFilter(django_filters.FilterSet):
    class Meta:
        model = Restaurant
        fields = {
            'name': ['icontains', 'contains'],
            # 'avg_rates': ['gt', 'lt', 'gte', 'lte'],
        }