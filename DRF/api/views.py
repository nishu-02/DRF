from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response # we pass the data
from rest_framework.decorators import api_view # function based views
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from api.filters import ProductFilter, InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

# Create your views here.

# so the interface we see on the browser it is beacuse of the render classes in the DRF

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True) # Instantitate the Product serializer
#     return Response(serializer.data) # Performs content negotiation on its own

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    # filterset_fields = ('name', 'price') # this will work only for quality based filtering (exact equal)
    filterset_fields = ProductFilter
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]
    
    search_fields = [
        '=name', """ with this = it will search for exact lookups """
        'description',
    ] # Case insensitive partial matching filter
    ordering_fields= [
        'name',
        'price'
    ]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2 #The number of response on the single page or in short the page size
    pagination_class.page_query_param = 'pagenum' 

    # Allowing the client to control the number of response on each page -> there exist a size query parameter for this
    pagination_class.max_page_size = 10

    # Limitoffsetpagination
    # pagination_class = LimitOffsetPagination #so it maps to we the one define in the settings
    
    def get_permissions(self):
        self.persmission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.persmission_classes == [IsAdminUser]
        return super().get_permissions()


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

class ProductDeatilAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id' # by default drf look for primary key in the url this is for the custom 

    def get_permissions(self):
        self.persmission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.persmission_classes == [IsAdminUser]
        return super().get_permissions()

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
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_prices': products.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(serializer.data)
