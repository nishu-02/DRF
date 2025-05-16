from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response # we pass the data
from rest_framework.decorators import api_view # function based views

# Create your views here.

# so the interface we see on the browser it is beacuse of the render classes in the DRF

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

@api_view(['GET'])
def Order_list(request):
    # orders = Order.objects.all()
    orders = Order.objects.prefetch_related(
        'items',
        'items_products'
        ).all() # prefetch_related is used to optimize the query
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_prices': products.aggregate(max_price=Max('price'))['max_price'],
    })
    return Response(serializer.data)
