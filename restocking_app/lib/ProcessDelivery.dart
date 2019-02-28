import 'package:flutter/material.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';
import 'package:http/http.dart' as http;

import 'model/Product.dart';
import 'model/Query.dart';
import 'model/Order.dart';

import 'Serializers.dart';

import 'utilities/ColourResolver.dart';
import 'utilities/Scan.dart';
import 'utilities/MakeRequest.dart';
import 'utilities/Toast.dart';

class ProcessDelivery extends StatelessWidget{
  final Query query;
  ProcessDelivery({@required this.query});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: MyHomePage(title: 'Process Delivery', query: this.query),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, @required this.query, this.title}) : super(key: key);
  final String title;
  final Query query;

  @override
  _MyHomePageState createState() => _MyHomePageState(query: query);
}

class _MyHomePageState extends State<MyHomePage> {
  final Query query;
  Order _order;

  _MyHomePageState({@required this.query});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        ),
      floatingActionButton: FloatingActionButton(
        child:Icon(MdiIcons.qrcodeScan),
        onPressed: ()async{processScan(await Scan.scan());}
      ),
      body: Center(
        child:FutureBuilder<Order>(
          future:MakeRequest.encodeOrder(this.query),
          builder: (context, snapshot){
            if (snapshot.hasData) {
              _order = snapshot.data;
              return buildList(createDeliveryList(snapshot.data));
            }else if (snapshot.hasError){
              return Text(snapshot.error);
            }
            return CircularProgressIndicator();
          }
        )
      ),
    );
  }

  ///Creates and returns the actual list that the user sees
  List<OrderItem> createDeliveryList(Order order){
    List<OrderItem> orderItem = new List<OrderItem>();

    for (var item in order.orderItems) {
      for (var i = 0; i < item.quantity - item.processed; i++) {
        orderItem.add(item);
      }      
    }

    return orderItem;
  }

  ///Builds the actual list that the user sees
  ListView buildList(List<OrderItem> deliveryList){
    return ListView.builder(
      itemCount: deliveryList.length,
      itemBuilder: (BuildContext context, int index){
        return new Card(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              ListTile(
                leading: Icon(
                  MdiIcons.shoeFormal,
                  color: ColorResolver.colorResolver(deliveryList[index].product.colour),
                  ),
                title: Text(deliveryList[index].product.name),
                subtitle: Text('Size ${deliveryList[index].product.size} ${deliveryList[index].product.fitting} in ${deliveryList[index].product.colour}'),
                trailing:IconButton(
                  icon: Icon(MdiIcons.delete),
                  onPressed: (){
                    updateOrderItem(deliveryList[index]);
                  },
                ) 
              ),
            ],
          )
        );
      },
    );
  }

  processScan(String productId) async{
    //TODO implement cancel
    //check if the product is a real product that exists.
    http.Response response = await MakeRequest.getRequest(Query(model: 'product', query: '$productId'));
    if (response.statusCode == 404){//product is not in the database.
      MyToast.showLongToast('Product not recognised');
    }else{
      //check if order is actually on the order
      response = await MakeRequest.getRequest(Query(model: 'order', query: '${_order.deliveryDate}/$productId'));
      print('${_order.deliveryDate}/$productId');
      if (response.statusCode == 200) {//Product is in the list, and we can process the order.
        //also need to check if the product should be deductable ie - it's in the product list.
        for (var item in _order.orderItems) {
          if (item.product.productId == int.parse(productId)){
            if (item.quantity - item.processed <=0) {
              //You shouldn't be scanning this product, but you can add another if you like!
              showDialog(
                context: context,
                builder: (BuildContext context){        
                  return AlertDialog(
                    title: Text('Order Discrepency'),
                    content: Text('Product ${item.product.name} size ${item.product.size} ${item.product.fitting} in ${item.product.colour} is on the delivery, but has already been processed ${item.processed}/${item.quantity} times. Do you want to add another?'),
                    actions: <Widget>[
                      new FlatButton(
                        child:Text('Cancel'),
                        onPressed: (){
                          Navigator.of(context).pop();
                          MyToast.showLongToast('${item.product.name} not added to order.');
                        },
                      ),
                      new RaisedButton(
                        textColor: Colors.white,
                        child:Text('Confirm'),
                        onPressed: (){
                          updateOrderItem(item);
                          Navigator.of(context).pop();
                        },
                      ),
                    ],
                  );
                });
            }else{
              //Product is fine to add to order.
              updateOrderItem(item);
            }
          }
        }
      }else if(response.statusCode == 404){//Product is not in the list, but we can add it!.
        OrderItem newOrderItem = Serializers.orderItemSerializer(int.parse(productId));
        showDialog(
          context: context,
          builder: (BuildContext context){        
            return AlertDialog(
              title: Text('Order Discrepency'),
              content: Text('Product ${newOrderItem.product.productId} is not on the delivery. Do you want to add it?'),
              actions: <Widget>[
                new FlatButton(
                  child:Text('Cancel'),
                  onPressed: (){
                    Navigator.of(context).pop();
                    MyToast.showLongToast('Product not added to order.');
                  },
                ),
                new RaisedButton(
                  textColor: Colors.white,
                  child:Text('Confirm'),
                  onPressed: (){
                    addOrderItem(newOrderItem);
                    Navigator.of(context).pop();
                  },
                ),
              ],
            );
          });
      }else{
        MyToast.showLongToast('Problem scanning stock: ${response.statusCode}');//most likely. 
      }
    }
  }

  updateOrderItem(OrderItem orderItem) async{
    http.Response response = await MakeRequest.patchRequest(
      Query(model: 'order', query:'${_order.orderId}/?format=json'), 
      Serializers.deserialiseOrderItemUpdate(orderItem.orderItemId, orderItem.processed + 1)
      );

    if (response.statusCode == 200) {
      MyToast.showLongToast('Scanned ${orderItem.product.name}');
      setState((){});//update state
    }else{
      MyToast.showLongToast('Could not update stock: ${response.statusCode}');
    }
  }

  addOrderItem(OrderItem orderItem) async{
    http.Response response =  await MakeRequest.postRequest(
      Query(model: 'order_item', query: 'create'), 
      Serializers.deserialiseOrderItemCreate(orderItem.product.productId, _order.orderId)
      );

    if (response.statusCode == 201) {
      MyToast.showLongToast('Scanned ${orderItem.product.name}');
      setState((){});//update state
    }else{
      MyToast.showLongToast('Could not update stock: ${response.statusCode}');
    }
  }
}