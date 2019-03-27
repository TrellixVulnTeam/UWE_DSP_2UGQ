import 'package:flutter/material.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';
import 'package:http/http.dart' as http;

import 'model/Query.dart';
import 'model/Order.dart';
import 'model/RestockingList.dart';

import 'Serializers.dart';
import 'utilities/ColourResolver.dart';
import 'utilities/MakeRequest.dart';
import 'utilities/Toast.dart';

class ShowProductRequests extends StatelessWidget{
  ShowProductRequests();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Restocking App',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: MyHomePage(title: 'Product Requests'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, @required this.title}) : super(key: key);
  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  _MyHomePageState();
  RestockingList _requests;

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child:FutureBuilder<RestockingList>(
          future: MakeRequest.recommendProduct(Query(model: 'stock_query', query: 'get')),
          builder: (context, snapshot){
            if(snapshot.hasData){
              _requests = snapshot.data;
              return buildList(_requests);
            }else if(snapshot.hasError){
              return Text(snapshot.error);
            }
            return CircularProgressIndicator();
          }
        )
      ),
    );
  }

  Widget buildList(RestockingList requests){
    return ListView.builder(
      itemCount: requests.restockingListItems.length,
      itemBuilder: (BuildContext context, int index){
        return new Card(
          child:Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              ListTile(
                title: Text(requests.restockingListItems[index].product.name),
                subtitle: RichText(
                  text: TextSpan(
                    style: TextStyle(
                      fontSize: 14.0,
                      color: Colors.black,
                    ),
                    children: <TextSpan>[
                      new TextSpan(text: 'Size '),
                      new TextSpan(text: '${requests.restockingListItems[index].product.size}', style: TextStyle(fontWeight: FontWeight.bold)),
                      new TextSpan(text: ' ${requests.restockingListItems[index].product.fitting} in '),
                      new TextSpan(
                        text: '${requests.restockingListItems[index].product.colour}', 
                        style: new TextStyle(
                          color: ColorResolver.colorResolver(requests.restockingListItems[index].product.colour), 
                          fontWeight: FontWeight.bold
                        )
                      ),
                    ]
                  ),
                ),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: <Widget>[
                    IconButton(
                      icon: Icon(MdiIcons.check),
                      onPressed: ()async{
                        MakeRequest.basicRequest(Query(model: 'stock_query', query: 'found/${requests.restockingListItems[index].product.productId}'));
                        setState((){});
                      },
                    ),
                    IconButton(
                      icon: Icon(MdiIcons.close),
                      onPressed: ()async{
                        MakeRequest.basicRequest(Query(model: 'stock_query', query: 'decrement/${requests.restockingListItems[index].product.productId}'));
                        setState((){});
                      },
                    ),
                    IconButton(
                      icon: Icon(MdiIcons.cancel),
                      onPressed: ()async{
                        MakeRequest.basicRequest(Query(model: 'stock_query', query: 'decrement/${requests.restockingListItems[index].product.productId}'));
                        setState((){});
                      },
                    ),
                  ],
                )
              )
            ],
          )
        );
      },
    );
  }

  static getProducts() async{
    Serializers.productSerializerRecommend(await MakeRequest.basicRequest(Query(model: 'stock_query', query: 'get')));
  }
}