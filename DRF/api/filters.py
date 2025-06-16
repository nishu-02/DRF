import django_filters
form api.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], # substring based lookups
            'price': ['exact', 'lt', 'gt', 'range'], # lower/greater & range based lookups
        }