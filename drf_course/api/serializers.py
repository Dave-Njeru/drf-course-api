from rest_framework import serializers
from . models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'stock',)

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        orders = obj.items.all()
        # return sum(order_item.item_subtotal for order_item in orders) == Generator expression to calculate total price of the order

        total = 0
        for order_item in orders:
            total += order_item.item_subtotal
        return total

    class Meta:
        model = Order
        fields = ('order_id', 'created_at', 'user', 'status', 'items', 'total_price')

# Flexible serializer for displaying products info
# Not tied to a specific model
class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True, read_only=True)
    count = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)