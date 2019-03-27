import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';

import 'utilities/MakeRequest.dart';
import 'Serializers.dart';
import 'model/Query.dart';
import 'StockQueryResults.dart';
import 'ShowProductRequests.dart';

import 'utilities/Scan.dart';
import 'utilities/Toast.dart';

import 'package:http/http.dart' as http;


class StockQueryForm{
  static Widget stockQueryForm(BuildContext context){
    final _stockFormKey = GlobalKey<FormState>();
    StockQuery stockQuery = new StockQuery();
    TextEditingController _nameController = new TextEditingController();
    TextEditingController _sizeController = new TextEditingController();

    return Center(
      child: Form(
        key:_stockFormKey,
        child: ListView(
          children: <Widget>[
            Padding(
              child:TextFormField(
                controller: _nameController,
                decoration: InputDecoration(
                  labelText: "Product Name"
                ),
              ),
              padding:EdgeInsets.fromLTRB(30, 30, 30, 0)
            ),
            //TODO validators
            Padding(
              child:TextFormField(
                controller: _sizeController,
                decoration: InputDecoration(
                  labelText: "Size"
                ),
                keyboardType: TextInputType.number,
              ),
              padding:EdgeInsets.fromLTRB(30, 30, 30, 0)
            ),
            Padding(
              child:RaisedButton(
                onPressed: () async {
                  if (_stockFormKey.currentState.validate()) {
                    var products = await validateProduct(StockQuery(name: _nameController.text, size: _sizeController.text));
                    if(products == false){
                      print(false);
                    }else{
                      Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => StockQueryResults(results: products)));
                    }
                  }
                },
                child:Text('Submit')
              ),
              padding:EdgeInsets.fromLTRB(30, 25, 30, 15)
            ),
            Padding(
              child:RaisedButton.icon(
                icon: Icon(MdiIcons.qrcodeScan),
                label: Text("Restock Product"),
                onPressed: ()async{processScan(await Scan.scan());},
              ),
              padding:EdgeInsets.fromLTRB(30, 25, 30, 10)
            ),
            Padding(
              child:RaisedButton.icon(
                icon: Icon(MdiIcons.voice),
                label: Text("View Stock Requests"),
                onPressed: (){
                  Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => ShowProductRequests()));
                },
              ),
              padding:EdgeInsets.fromLTRB(30, 0, 30, 30)
            )
          ],
        )
      ),
    );
  }

  static dynamic validateProduct(StockQuery query) async{
    var sizes = query.size.split('.');
    print(sizes);
    var name = query.name.replaceAll(" ", "_");
    String queryText = '$name/${sizes[0]}/${sizes[1]}';
    print(queryText);
    var responseBody = await MakeRequest.basicRequest(Query(model: 'stock_query', query: queryText));
    print(responseBody);
    if(responseBody == 'Failure'){
      return false;
    }else{
      return Serializers.productSerializerRecommend(responseBody);
    }
  }

  static processScan(String productId) async{
    //TODO implement cancel
    //check if the product is a real product that exists.
    http.Response response = await MakeRequest.getRequest(Query(model: 'product', query: '$productId'));
    if (response.statusCode == 404){//product is not in the database.
      MyToast.showLongToast('Product not recognised');
    }else{
      MakeRequest.basicRequest(Query(model: 'stock_query', query: 'restock/$productId'));
    }
  }
}

class StockQuery{
  String name;
  String size;

  StockQuery({this.name, this.size});
}