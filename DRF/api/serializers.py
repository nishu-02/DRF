from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    # its gonna look at the model and it is smart enough to get the dataType, and also gonna do the validation
    class Meta:
        model = Product
        fields = (
            # 'id', we can create a separate serializer if we wish to return the id  
            'name',
            'description',
            'price',
            'stock',
        )

    # The validation function on the price 
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0"
            )
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    # if we wish to flatten the data
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price'
        )
    class Meta:
        model = OrderItem
        fields = (
            # 'product',
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) # so we want this when we are fetching the orders not when creating one
    # removing the realted_name return the primary key of the items

    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self.obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user', # It is the foreign key here
            'status',
            'items',
            'total_price',
        )

# Generic serializers

class ProductInfoSerializer(serializers.ModelSerializer):
    # get all products, count of products, max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()  