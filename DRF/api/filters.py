import django_filters
from api.models import Product, Order
from rest_framework import filters

class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
        
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], # substring based lookups
            'price': ['exact', 'lt', 'gt', 'range'], # lower/greater & range based lookups
        }

class OrderFilter(django_filters.FilterSet):
    created_at = djnago_filters.DateFilter(field_name='created_at__date')
    # by default the time is midnight on the date basis filter so we just extract the date from the whole date and time string
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at: ['lt', 'gt', 'exact']
        }