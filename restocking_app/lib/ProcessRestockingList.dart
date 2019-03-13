import 'package:flutter/material.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';
import 'package:http/http.dart' as http;

import 'model/Query.dart';
import 'model/RestockingList.dart';

import 'Serializers.dart';

import 'utilities/MakeRequest.dart';
import 'utilities/ListSorter.dart';
import 'utilities/ProductCodeResolver.dart';
import 'utilities/ColourResolver.dart';
import 'utilities/Scan.dart';
import 'utilities/Toast.dart';

class ProcessRestockingList extends StatelessWidget{
  final Query query;
  ProcessRestockingList({@required this.query});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Restocking App',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: MyHomePage(title: 'Process Restocking List', query: this.query),
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
  RestockingList _restockingList;
  String _filter;

  _MyHomePageState({@required this.query});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar:AppBar(
        title: Text(widget.title),
        actions: <Widget>[
          PopupMenuButton(
            icon: Icon(MdiIcons.filter),
            itemBuilder: (_) => <PopupMenuItem<String>>[
              new PopupMenuItem<String>(
                child: const Text('Filter by Name'), value: 'name'),
              new PopupMenuItem<String>(
                child: const Text('Filter by Department (Childrens)'), value: 'childrens'),
              new PopupMenuItem<String>(
                child: const Text('Filter by Department (Ladies)'), value: 'ladies'),
              new PopupMenuItem<String>(
                child: const Text('Filter by Department (Mens)'), value: 'mens'),
              new PopupMenuItem<String>(
                child: const Text('Filter by Size'), value: 'size'),
            ],
            onSelected: (String result){
              setState((){_filter=result;});
            },
          )
        ]
      ),
      body:Center(
        child:FutureBuilder<RestockingList>(
          future:MakeRequest.encodeRestockingList(this.query),
          builder: (context, snapshot){
            if(snapshot.hasData){
              _restockingList = snapshot.data;
              if (_filter != null) {
                ListSorter.sortRestockingList(_restockingList, _filter);
              }
              return buildList(createRestockingList(_restockingList));
            }else if(snapshot.hasError){
              return Text(snapshot.error);
            }
            return CircularProgressIndicator();
          }
        )
      ),
      floatingActionButton: FloatingActionButton(
        child:Icon(MdiIcons.qrcodeScan),
        onPressed: ()async{processScan(await Scan.scan());}
      ),
    );
  }

  List<RestockingListItem> createRestockingList(RestockingList restockingList){
    List<RestockingListItem> restockingListItems = new List<RestockingListItem>();

    for (var item in restockingList.restockingListItems) {
      for (var i = 0; i < item.quantity - item.processed; i++) {
        restockingListItems.add(item);
      }      
    }
    
    if(restockingListItems.isEmpty){
      print('Restocking List Is Empty');
    }

    return restockingListItems;
  }

  ListView buildList(List<RestockingListItem> restockingList){
    return ListView.builder(
      itemCount: restockingList.length,
      itemBuilder: (BuildContext, int index){
        return new Card(
          child:Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              ListTile(
                leading: Icon(
                  ProductCodeResolver.productCodeResolver(restockingList[index].product.productCode),
                  color: ColorResolver.colorResolver(restockingList[index].product.colour)
                  ),
                title: Text(restockingList[index].product.name),
                subtitle: Text('Size ${restockingList[index].product.size} ${restockingList[index].product.fitting} in ${restockingList[index].product.colour}'),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: <Widget>[
                    IconButton(
                      icon: Icon(MdiIcons.exclamation),
                      onPressed: (){
                        recommendProducts(restockingList[index]);
                      },
                    ),
                    IconButton(
                      icon: Icon(MdiIcons.check),
                      onPressed: (){
                        updateRestockingListItem(restockingList[index]);
                      },
                    )
                  ],
                )
              )
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
      //check if order is actually on the restocking list
      response = await MakeRequest.getRequest(Query(model: 'restocking', query: '${_restockingList.date}/${_restockingList.time}/$productId'));
      if (response.statusCode == 200) {//Product is in the list, and we can process the order.
        //also need to check if the product should be deductable ie - it's in the product list.
        for (var item in _restockingList.restockingListItems) {
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
                          updateRestockingListItem(item);
                          Navigator.of(context).pop();
                        },
                      ),
                    ],
                  );
                });
            }else{
              //Product is fine to add to order.
              updateRestockingListItem(item);
            }
          }
        }
      }else if(response.statusCode == 404){//Product is not in the list, but we can add it!.
        RestockingListItem newRestockingListItem = Serializers.restockingListItemSerializer(int.parse(productId));
        showDialog(
          context: context,
          builder: (BuildContext context){        
            return AlertDialog(
              title: Text('Restocking List Discrepency'),
              content: Text('Product ${newRestockingListItem.product.productId} is not on the restocking list. Do you want to add it?'),
              actions: <Widget>[
                new FlatButton(
                  child:Text('Cancel'),
                  onPressed: (){
                    Navigator.of(context).pop();
                    MyToast.showLongToast('Product not added to Restocking List.');
                  },
                ),
                new RaisedButton(
                  textColor: Colors.white,
                  child:Text('Confirm'),
                  onPressed: (){
                    addRestockingListItem(newRestockingListItem);
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

  updateRestockingListItem(RestockingListItem restockingListItem) async{
    //update restocking list
    http.Response response = await MakeRequest.patchRequest(
      Query(model: 'restocking', query:'${_restockingList.restockingListId}/?format=json'), 
      Serializers.deserialiseRestockingListItemUpdate(
          restockingListItem.restockingListItemId,
          restockingListItem.processed + 1, 
          restockingListItem.product.productId,
          _restockingList.restockingListId
        )
    );

    if (response.statusCode == 200) {
      response = await MakeRequest.patchRequest(
      Query(model: 'product', query:'${restockingListItem.product.productId}/?format=json'), 
      Serializers.deserialiseProductUpdate(
        restockingListItem.product.productId,
        restockingListItem.product.stockQuantity - 1,
        restockingListItem.product.stockQuantity + 1,
        )
      );
      if(response.statusCode == 200){
        MyToast.showLongToast('Scanned ${restockingListItem.product.name}');
        setState((){});//update state
      }else{
        MyToast.showLongToast('Could not update stock');
        //reverse our terrible decisions
        http.Response response = await MakeRequest.patchRequest(
        Query(model: 'restocking', query:'${_restockingList.restockingListId}/?format=json'), 
        Serializers.deserialiseRestockingListItemUpdate(
          restockingListItem.restockingListItemId,
          restockingListItem.processed - 1, 
          restockingListItem.product.productId,
          _restockingList.restockingListId
          )        
        );
      }
    }else{
      MyToast.showLongToast('Could not update stock: ${response.statusCode}');
    }
  }

  addRestockingListItem(RestockingListItem restockingListItem) async{
    http.Response response =  await MakeRequest.postRequest(
      Query(model: 'order_item', query: 'create'), 
      Serializers.deserialiseOrderItemCreate(restockingListItem.product.productId, _restockingList.restockingListId)
      );

    if (response.statusCode == 201) {
      MyToast.showLongToast('Scanned ${restockingListItem.product.name}');
      setState((){});//update state
    }else{
      MyToast.showLongToast('Could not add stock: ${response.statusCode}');
    }
  }

  recommendProducts(RestockingListItem restockingListItem) async{
    RestockingList _products;
    showDialog(
      context: context,
      builder: (BuildContext context){    
        return AlertDialog(
          title: Text('Product Not In Stock'),
          content: Column(
            children: <Widget>[
              Text('${restockingListItem.product.name} has not been found. Please pull one of the products below.'),
              Container(
                padding: EdgeInsets.fromLTRB(0, 10, 0, 0),
                height: 300,
                width: 300,
                child:FutureBuilder<RestockingList>(
                  future:MakeRequest.recommendProduct(Query(model: 'recommend', query: restockingListItem.restockingListItemId.toString())),
                  builder: (context, snapshot){
                  if(snapshot.hasData){
                    _products = snapshot.data;
                    return buildRecommendList(createRecommendList(_products));
                  }else if(snapshot.hasError){
                    return Text(snapshot.error);
                  }
                  return CircularProgressIndicator();
                  }
                ) 
              )       
            ],
          ),
          actions: <Widget>[
            new FlatButton(
              child:Text('Cancel'),
              onPressed: (){
                Navigator.of(context).pop();
              },
            ),
            new RaisedButton(
              textColor: Colors.white,
              child:Text('Remove Product From List'),
              onPressed: (){
                MakeRequest.basicRequest(Query(model: 'recommend', query: 'remove/${restockingListItem.restockingListItemId}'));
                setState(() {});
                Navigator.of(context).pop();
                MyToast.showLongToast('Please scan recommended product.');
              },
            ),
          ],
        );
      }
    );   
  }
ListView buildRecommendList(List<RestockingListItem> restockingList){
    return ListView.builder(
      shrinkWrap: true,
      itemCount: restockingList.length,
      itemBuilder: (BuildContext, int index){
        return new Card(
          child:Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              ListTile(
                leading: Icon(
                  ProductCodeResolver.productCodeResolver(restockingList[index].product.productCode),
                  color: ColorResolver.colorResolver(restockingList[index].product.colour)
                  ),
                title: Text(restockingList[index].product.name),
                subtitle: Text('Size ${restockingList[index].product.size} ${restockingList[index].product.fitting} in ${restockingList[index].product.colour}'),
              )
            ],
          )
        );
      },
    );
  }

  List<RestockingListItem> createRecommendList(RestockingList restockingList){
    List<RestockingListItem> restockingListItems = new List<RestockingListItem>();

    for (var item in restockingList.restockingListItems) {
        restockingListItems.add(item);    
    }
    
    if(restockingListItems.isEmpty){
      print('Restocking List Is Empty');
    }

    return restockingListItems;
  }


}


