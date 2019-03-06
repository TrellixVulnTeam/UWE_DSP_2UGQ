import 'package:flutter/material.dart';

import 'package:http/http.dart' as http;

import 'model/Query.dart';
import 'model/RestockingList.dart';

import 'utilities/MakeRequest.dart';
import 'utilities/ListCreation.dart';

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

  _MyHomePageState({@required this.query});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar:AppBar(
        title: Text(widget.title),
      ),
      body:Center(
        child:FutureBuilder<RestockingList>(
          future:MakeRequest.encodeRestockingList(this.query),
          builder: (context, snapshot){
            if(snapshot.hasData){
              _restockingList = snapshot.data;
              return buildList(createRestockingList(snapshot.data));
            }else if(snapshot.hasError){
              return Text(snapshot.error);
            }
            return CircularProgressIndicator();
          }
        )
      )
    );
  }

  List<RestockingListItem> createRestockingList(RestockingList restockingList){
    List<RestockingListItem> restockingListItems = new List<RestockingListItem>();

    for (var item in restockingList.restockingListItems) {
      for (var i = 0; i < item.quantity - item.processed; i++) {
        restockingListItems.add(item);
      }      
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
                title: Text(restockingList[index].product.name),
                subtitle: Text('Size ${restockingList[index].product.size} ${restockingList[index].product.fitting} in ${restockingList[index].product.colour}'),
              )
            ],
          )
        );
      },
    );
  }
}