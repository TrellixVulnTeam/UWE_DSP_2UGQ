import 'model/Order.dart';
import 'model/Product.dart';
import 'model/RestockingList.dart';
import 'dart:convert';

class Serializers {
  static Order orderSerializer(String responseBody){
    Map<String, dynamic> data = json.decode(responseBody);

    List<OrderItem> orderItems = new List<OrderItem>();

    for (var item in data['order_items']) {
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
          stockQuantity: item['product']['stock_quantity'],
          floorQuantity: item['product']['floor_quantity']
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
      stockQuantity: data['stock_quantity'],
      floorQuantity: data['floor_quantity']
    );
  }

  static RestockingList restockingListSerializer(String responseBody){
    Map<String, dynamic> data = json.decode(responseBody);

    List<RestockingListItem> restockingListItems = new List<RestockingListItem>();

    for (var item in data['restocking_items']) {
      restockingListItems.add(RestockingListItem(
        restockingListItemId: item['id'],
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
          stockQuantity: item['product']['stock_quantity'],
          floorQuantity: item['product']['floor_quantity']
        )
      ));
    }

    return RestockingList(
      restockingListId: data['id'],
      date: data['date'],
      time: data['time'],
      restockingListItems: restockingListItems
    );
  }

  static String deserialiseOrderItemUpdate(int itemId, int processed){ 
    var jsonMap = {
      "order_items": [
        {
          "id": itemId,
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

  static String deserialiseRestockingListItemUpdate(int itemId, int processed, int productId, int restockingListId){ 
    var jsonMap = {
      "restocking_items":[
        {
          "id":itemId,
          "processed":processed,
          "product":{
            "id":productId
          },
          "restocking_list":restockingListId
        }
      ]
    };
    return jsonEncode(jsonMap);
  }

  static String deserialiseRestockingListItemCreate(int productId, int restockingListId){
    var jsonMap = {
      "restocking_list": restockingListId,
      "quantity" : 1,
      "processed" : 1,
      "product" : {
        "id" : productId
      }
    };
    return jsonEncode(jsonMap);
  }

  static RestockingListItem restockingListItemSerializer(int productId){
    return RestockingListItem(
      product: Product(productId: productId),
      quantity: 1,
      processed: 1
    );
  }

  static String deserialiseProductUpdate(int productId, int stockQuantity, int floorQuantity){
    var jsonMap = {
      "id": productId,
      "stock_quantity": stockQuantity,
      "floor_quantity": floorQuantity 
    };
    return jsonEncode(jsonMap);
  }

  static RestockingList productSerializerRecommend(String responseBody){
    Map<String, dynamic> data = json.decode(responseBody);

    List<RestockingListItem> restockingListItems = new List<RestockingListItem>(); 

    for (var item in data['recommendations']) {
      restockingListItems.add(
        RestockingListItem(
          product: Product(
            productId: item['id'],
            name: item['name'],
            size: double.parse(item['size']),
            colour: item['colour'],
            fitting: item['fitting'],
            price: item['price'],
            sale: item['sale'],
            productType: item['product_type'],
            productCode: item['product_code'],
            department: item['department'],
            floorQuantity: item['floor_quantity'],
            stockQuantity: item['stock_quantity']
          )
        )
      );
    }
    print(restockingListItems[0].product);
    return RestockingList(restockingListItems:restockingListItems);
  }
}