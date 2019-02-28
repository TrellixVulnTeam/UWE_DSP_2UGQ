from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    """Serializer to map a model into JSON format"""

    id=serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'size', 'colour', 'fitting', 'price', 'sale', 'product_type', 'product_code', 'department', 'stock_quantity')
        read_only_fields = ('name', 'size', 'colour', 'fitting', 'price', 'sale', 'product_type', 'product_code', 'department', 'stock_quantity')

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    id=serializers.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = ('id', 'quantity', 'product', 'processed', 'order')
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer to map a model into JSON Format for Orders"""
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_processed', 'order_delivered', 'delivery_date', 'delivery_time', 'delivery_processed', 'items')
        read_only_fields = ('id', 'order_processed', 'order_delivered', 'delivery_date', 'delivery_time', 'delivery_processed')

    def update(self, instance, validated_data):
        items =  validated_data.get('items')
        for item in items:
            item_id = item.get('id', None)
            order_item = OrderItem.objects.get(id__exact=item_id)
            order_item.processed = item.get('processed', order_item.processed)
            order_item.quantity = item.get('quantity', order_item.quantity)
            order_item.save()

        return instance