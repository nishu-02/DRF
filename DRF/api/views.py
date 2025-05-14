from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response # we pass the data
from rest_framework.decorators import api_view # function based views

# Create your views here.

# so the interface we see on the broweser it is beacuse of the render classes in the DRF

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) # Instantitate the Product serializer
    return Response(serializer.data) # Performs content negotiation on its own


@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

