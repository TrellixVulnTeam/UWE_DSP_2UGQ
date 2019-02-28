import 'Product.dart';

class Order {
  final int orderId;
  final bool orderProcessed;
  final bool orderDelivered;
  final String deliveryDate;
  final bool deliveryProcessed;
  final List<OrderItem> orderItems;

  Order({this.orderId, this.orderProcessed, this.orderDelivered, this.deliveryDate, this.deliveryProcessed, this.orderItems});
}

class OrderItem{
  final int orderItemId;
  final int quantity;
  final int processed;
  final Product product;

  OrderItem({this.orderItemId, this.quantity, this.processed, this.product});
}