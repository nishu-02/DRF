from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response # we pass the data
from rest_framework.decorators import api_view # function based views
from rest_framework import generics
from rest_framework.persmissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
# Create your views here.

# so the interface we see on the browser it is beacuse of the render classes in the DRF

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True) # Instantitate the Product serializer
#     return Response(serializer.data) # Performs content negotiation on its own

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.persmission_classes = [AllowAny]
        if self.request.method == 'POST'
            self.persmission_classes == [IsAdminUser]
        return super().get_permissions


# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer

#     def create(self, request, *args, **kwargs): # overwritng the default method
#         print(request.data)
#         return super().create(request, *args, **kwargs)

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class ProductDeatilAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id' # by default drf look for primary key in the url this is for the custom 

# @api_view(['GET'])
# def Order_list(request):
#     # orders = Order.objects.all()
#     orders = Order.objects.prefetch_related(
#         'items',
#         'items_products'
#         ).all() # prefetch_related is used to optimize the query
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

# class OrderListAPIView(generics.ListAPIView): # generic view
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    persmission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset() # or self.queryset basically it refers to the parent class method
        return qs.filter(user=user)

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         'max_prices': products.aggregate(max_price=Max('price'))['max_price'],
#     })
#     return Response(serializer.data)

class ProductInfoAPIView(APIView):
    def get(self. request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_prices': products.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(serializer.data)
