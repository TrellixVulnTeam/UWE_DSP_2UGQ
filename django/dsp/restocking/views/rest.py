"""
Contains views relating to the rest part of the project.
"""

from rest_framework import generics
from restocking.serializers import ProductSerializer, OrderSerializer,  OrderItemSerializer
from restocking.models import Product, Order, OrderItem


class DetailsViewOrder(generics.RetrieveUpdateAPIView):
    """Handles GET, PUT and DELETE for orders"""
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

class DetailsViewOrderByDate(generics.RetrieveUpdateAPIView):
    """Handles GET, PUT and DELETE for products by date"""
    serializer_class = OrderSerializer
    lookup_field = 'delivery_date'

    def get_queryset(self):
        delivery_date = self.kwargs['delivery_date']
        return Order.objects.filter(delivery_date__exact=delivery_date)

class DetailsViewOrderByDateFilterProduct(generics.RetrieveUpdateAPIView):
    """Handles GET, PUT and DELETE for products by date and by product id"""
    serializer_class = OrderSerializer
    lookup_field = 'delivery_date'

    def get_queryset(self):
        delivery_date = self.kwargs['delivery_date']
        product = self.kwargs['product_id']
        if product is not None:
            try:
                query = Order.objects.filter(
                    delivery_date__exact=delivery_date, 
                    id__exact=OrderItem.objects.get(product__exact=product).order.id
                )
            except Exception as exception:
                if exception == 'OrderItem matching query does not exist.':
                    return None
                else:
                    raise exception

            return query

class CreateOrderItemView(generics.ListCreateAPIView):
    """Handles POST"""
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.all()

    def perform_create(self, serializer):
        OrderItem(
            order=Order.objects.get(id__exact=serializer.data['order']),
            quantity=serializer.data['quantity'],
            processed=serializer.data['processed'],
            product=Product.objects.get(id__exact=serializer['product']['id'].value)
        ).save()

class DetailsViewProduct(generics.RetrieveUpdateAPIView):
    """Handles GET, PUT and DELETE for products"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()