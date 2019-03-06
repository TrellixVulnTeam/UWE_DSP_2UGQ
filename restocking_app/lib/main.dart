import 'package:flutter/material.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';

import 'OrderQueryForm.dart';
import 'RestockingQueryForm.dart';

void main() => runApp(MyMain());

class MyMain extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: MyHomePage(title: 'Generic Shoe Company'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child:Scaffold(
        appBar: AppBar(
          bottom: TabBar(
            tabs: <Widget>[
              Tab(text: 'Deliveries'),
              Tab(text: 'Restocking'),
              Tab(text: 'Stock Check'),
            ],
          ),
          title: Text(widget.title),
        ),
        body: TabBarView(
          children: <Widget>[
            OrderQueryForm.orderQueryForm(context),
            RestockingQueryForm.restockingQueryForm(context),
            Icon(Icons.access_alarms),
          ],
        )
      )
    );
  }
}


