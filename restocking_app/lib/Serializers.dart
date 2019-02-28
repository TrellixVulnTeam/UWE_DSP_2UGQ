import 'model/Order.dart';
import 'model/Product.dart';
import 'dart:convert';

class Serializers {
  static Order orderSerializer(String responseBody){
    Map<String, dynamic> data = json.decode(responseBody);

    List<OrderItem> orderItems = new List<OrderItem>();

    for (var item in data['items']) {
      orderItems.add(OrderItem(
        orderItemId: item['id'],
        quantity: item['quantity'],
        processed: item['processed'],
        product: Product(
          productId: item['product']['id'],
          name: item['product']['name'],
          size: item['product']['size'],
          colour: item['product']['colour'],
          fitting: item['product']['fitting'],
          price: item['product']['price'],
          sale: item['product']['sale'],
          productType: item['product']['product_type'],
          productCode: item['product']['product_code'],
          department: item['product']['department'],
          stockQuantity: item['product']['stock_quantity']
        ),
      ));
    }

    Order order = Order(
      orderId: data['id'],
      orderProcessed: data['order_processed'],
      orderDelivered: data['order_delivered'],
      deliveryDate: data['delivery_date'],
      orderItems: orderItems,
    );

    return order;
  }
  
  //Not actually tested yet don't blame me if it breaks.
  static Product productSerializer(String responseBody){
    Map<String, dynamic> data = json.decode(responseBody);

    return Product(
      productId: data['id'],
      name: data['name'],
      size: data['size'],
      colour: data['colour'],
      fitting: data['fitting'],
      price: data['price'],
      sale: data['sale'],
      productType: data['product_type'],
      productCode: data['product_code'],
      department: data['department'],
      stockQuantity: data['stock_quantity']
    );
  }

  static String deserialiseOrderItemUpdate(int orderItemid, int processed){
    var jsonMap = {
      "items": [
        {
          "id": orderItemid,
          "processed":processed,
        }
      ]
    };
    return jsonEncode(jsonMap);
  }

  static String deserialiseOrderItemCreate(int productId, int orderId){
    var jsonMap = {
      "order": orderId,
      "quantity" : 1,
      "processed" : 1,
      "product" : {
        "id" : productId
      }
    };
    return jsonEncode(jsonMap);
  }

  static OrderItem orderItemSerializer(int productId){
    return OrderItem(
      product: Product(productId: productId),
      quantity: 1,
      processed: 1
    );
  }
}