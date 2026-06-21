import django_filters
from api.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],  # Filter by name (case-insensitive)
            'price': ['exact', 'lt', 'gt', 'range']  # Filter by price (exact, less than, greater than, range)
        }