from rest_framework import serializers
from .models import Product, Order, OrderItem, RestockingList, RestockingListItem

class ProductSerializer(serializers.ModelSerializer):
    """Serializer to map a model into JSON format"""

    id=serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'size', 'colour', 'fitting', 'price', 'sale', 'product_type', 'product_code', 'department', 'stock_quantity', 'floor_quantity')
        read_only_fields = ('name', 'size', 'colour', 'fitting', 'price', 'sale', 'product_type', 'product_code', 'department')

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    id = serializers.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = ('id', 'quantity', 'product', 'processed', 'order', 'added')
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer to map a model into JSON Format for Orders"""
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_processed', 'order_delivered', 'delivery_date', 'delivery_processed', 'order_items')
        read_only_fields = ('id', 'order_processed', 'order_delivered', 'delivery_date', 'delivery_processed')

    def update(self, instance, validated_data):
        print(validated_data)
        items = validated_data.get('order_items')
        for item in items:
            item_id = item.get('id', None)
            order_item = OrderItem.objects.get(id__exact=item_id)
            order_item.processed = item.get('processed', order_item.processed)
            order_item.quantity = item.get('quantity', order_item.quantity)
            order_item.save()

        return instance

class RestockingListItemSerializer(serializers.ModelSerializer):
    """Serializer to map a model into JSON format for restocking list items"""
    product = ProductSerializer()

    id = serializers.IntegerField(required=False)

    class Meta:
        model = RestockingListItem
        fields = ('id', 'quantity', 'product', 'processed', 'restocking_list', 'added')
        read_only_fields = ['id']

class RestockingListSerializer(serializers.ModelSerializer):
    """Serializer to map a model into JSON format for restocking lists"""
    restocking_items = RestockingListItemSerializer(many=True)

    class Meta:
        model = RestockingList
        fields = ('id', 'date', 'time', 'restocking_items', 'datetime')
        read_only_fields = ('id', 'date', 'time', 'datetime')

    def update(self, instance, validated_data):
        restocking_list_items = validated_data.get('restocking_items')
        for item in restocking_list_items:
            item_id = item.get('id', None)
            restocking_list_item = RestockingListItem.objects.get(id__exact=item_id)
            restocking_list_item.processed = item.get('processed', restocking_list_item.processed)
            restocking_list_item.quantity = item.get('quantity', restocking_list_item.quantity)
            restocking_list_item.save()

        return instance


def serialize_recommendation(candidates):
    """
    Serialises our recommendations into a list of products.
    """
    dictionary = {}
    dictionary['recommendations'] = []
    for index, item in enumerate(list(candidates)):
        dictionary['recommendations'].append({})
        dictionary['recommendations'][index]['id'] = item.id
        dictionary['recommendations'][index]['name'] = item.name
        dictionary['recommendations'][index]['size'] = str(item.size)
        dictionary['recommendations'][index]['colour'] = item.colour
        dictionary['recommendations'][index]['fitting'] = item.fitting
        dictionary['recommendations'][index]['price'] = str(item.price)
        dictionary['recommendations'][index]['sale'] = item.sale
        dictionary['recommendations'][index]['product_type'] = item.product_type
        dictionary['recommendations'][index]['product_code'] = item.product_code
        dictionary['recommendations'][index]['department'] = item.department
        dictionary['recommendations'][index]['floor_quantity'] = item.floor_quantity
        dictionary['recommendations'][index]['stock_quantity'] = item.stock_quantity

    return dictionary