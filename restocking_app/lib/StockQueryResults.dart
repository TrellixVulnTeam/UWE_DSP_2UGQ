import 'package:flutter/material.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';
import 'package:http/http.dart' as http;

import 'model/Query.dart';
import 'model/Order.dart';
import 'model/RestockingList.dart';

import 'utilities/ColourResolver.dart';
import 'utilities/MakeRequest.dart';
import 'utilities/Toast.dart';

class StockQueryResults extends StatelessWidget{
  final RestockingList results;
  StockQueryResults({@required this.results});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Restocking App',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: MyHomePage(title: 'Query Results', results: this.results),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, @required this.results, this.title}) : super(key: key);
  final String title;
  final RestockingList results;

  @override
  _MyHomePageState createState() => _MyHomePageState(results: results);
}

class _MyHomePageState extends State<MyHomePage> {
  final RestockingList results;

  _MyHomePageState({@required this.results});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child:buildList()
      ),
    );
  }

  Widget buildList(){
    return ListView.builder(
      itemCount: results.restockingListItems.length,
      itemBuilder: (BuildContext context, int index){
        return new Card(
          child:Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              ListTile(
                title: Text(results.restockingListItems[index].product.name + " (${results.restockingListItems[index].product.stockQuantity.toString()})"),
                subtitle: RichText(
                  text: TextSpan(
                    style: TextStyle(
                      fontSize: 14.0,
                      color: Colors.black,
                    ),
                    children: <TextSpan>[
                      new TextSpan(text: 'Size '),
                      new TextSpan(text: '${results.restockingListItems[index].product.size}', style: TextStyle(fontWeight: FontWeight.bold)),
                      new TextSpan(text: ' ${results.restockingListItems[index].product.fitting} in '),
                      new TextSpan(
                        text: '${results.restockingListItems[index].product.colour}', 
                        style: new TextStyle(
                          color: ColorResolver.colorResolver(results.restockingListItems[index].product.colour), 
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
                      icon: Icon(MdiIcons.voice),
                      onPressed: ()async{
                        MakeRequest.basicRequest(Query(model: 'stock_query', query:'increment/${results.restockingListItems[index].product.productId}'));
                        MyToast.showLongToast("Product Requested");
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
}