from django.http import JsonResponse
from api.serializers import ProductSerializer
from api.models import Product

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) # Instantitate the Product serializer
    return JsonResponse({
        'data': serializer.data
    })