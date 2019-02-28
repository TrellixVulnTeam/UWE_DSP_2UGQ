import 'package:flutter/material.dart';

import 'package:datetime_picker_formfield/datetime_picker_formfield.dart';
import 'package:intl/intl.dart';
import 'package:fluttertoast/fluttertoast.dart';

import 'utilities/MakeRequest.dart';
import 'ProcessDelivery.dart';
import 'model/Query.dart';

import 'package:http/http.dart' as http;


class OrderQueryForm{
  static Widget orderQueryForm(BuildContext context){
    final _deliveryFormKey = GlobalKey<FormState>();
    OrderQuery orderQuery = new OrderQuery();

    return Center(
      child: Form(
        key:_deliveryFormKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Padding(
              child: DateTimePickerFormField(
                inputType: InputType.date,
                format: DateFormat('yyyy-MM-dd'),
                editable: true,
                validator: (value){
                  if (value.toString() == 'null') {
                    return 'Please enter a date';
                  }
                },
                decoration: InputDecoration(
                  hintText: 'Delivery Date',
                ),
                onChanged:(value){
                  orderQuery.date = value;
                },
              ),
              padding:EdgeInsets.fromLTRB(30, 30, 30, 0)
            ),
            Padding(
              child:RaisedButton(
                onPressed: () async {
                  if (_deliveryFormKey.currentState.validate()) {
                    http.Response response = await MakeRequest.getRequest(Query(model: 'order', query: orderQuery.date.toString().split(' ')[0]));
                    if (response.statusCode == 404) {
                      Fluttertoast.showToast(
                        msg: "Can't find a delivery on that date.",
                        toastLength: Toast.LENGTH_LONG,
                      );                      
                    }else if(response.statusCode != 200){
                      Fluttertoast.showToast(
                        msg: "Something has gone horribly wrong. Please contact administration.",
                        toastLength: Toast.LENGTH_LONG,
                      ); 
                    }else{
                      //view delivery with response.
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => ProcessDelivery(query: Query(model: 'order', query: orderQuery.date.toString().split(' ')[0]))),
                      );
                    }
                  }
                },
                child:Text('Submit')
              ),
              padding:EdgeInsets.fromLTRB(30, 25, 30, 30)
            )
          ],
        )
      ),
    );
  }
}

class OrderQuery{
  DateTime date;

  OrderQuery({this.date});
}