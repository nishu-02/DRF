from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    # its gonna look at the model and it is smart enough to get the dataType, and also gonna do the validation
    class Meta:
        model = Product
        fields = (
            'id',
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
    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) # so we want this when we are fetching the orders not when creating one
    
    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user', # It is the foreign key here
            'status',
            'items',
        )
