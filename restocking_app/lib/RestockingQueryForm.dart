import 'package:flutter/material.dart';

import 'package:datetime_picker_formfield/datetime_picker_formfield.dart';
import 'package:intl/intl.dart';
import 'package:fluttertoast/fluttertoast.dart';

import 'utilities/MakeRequest.dart';
import 'utilities/Toast.dart';
import 'model/Query.dart';
import 'ProcessRestockingList.dart';

import 'package:http/http.dart' as http;

class RestockingQueryForm{
  static Widget restockingQueryForm(BuildContext context){
    final _deliveryFormKey = GlobalKey<FormState>();
    RestockingQuery restockingQuery = new RestockingQuery();

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
                  hintText: 'Restocking Date',
                ),
                onChanged:(value){
                  restockingQuery.date = value;
                },
              ),
              padding:EdgeInsets.fromLTRB(30, 30, 30, 0)
            ),
            Padding(
              child: DateTimePickerFormField(
                format: DateFormat("HH:mm"),
                inputType: InputType.time,
                editable: true,
                validator: (value){
                  if (value.toString() == 'null') {
                    return 'Please enter a time';
                  }
                },
                decoration: InputDecoration(
                  hintText: 'List Time',
                ),
                onChanged:(value){
                  restockingQuery.time = value;
                },
              ),
              padding:EdgeInsets.fromLTRB(30, 30, 30, 0)
            ),
            Padding(
              child:RaisedButton(
                onPressed: () async {
                  if (_deliveryFormKey.currentState.validate()) {
                    String qry = "${restockingQuery.date.year}-${restockingQuery.date.month}-${restockingQuery.date.day}/${restockingQuery.time.hour.toString()}-${restockingQuery.time.minute.toString()}";
                    print(qry);
                    http.Response response = await MakeRequest.getRequest(Query(model: 'restocking', query: qry));
                    if (response.statusCode == 404) {
                      Fluttertoast.showToast(
                        msg: "Can't find a restocking list on that time.",
                        toastLength: Toast.LENGTH_LONG,
                      );                      
                    }else if(response.statusCode != 200){
                      print(response.statusCode);
                      Fluttertoast.showToast(
                        msg: "Something has gone horribly wrong. Please contact administration.",
                        toastLength: Toast.LENGTH_LONG,
                      ); 
                    }else{
                      //view list with response.
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => ProcessRestockingList(query: Query(model: 'restocking', query: qry))),
                      );
                    }
                  }
                },
                child:Text('Submit')
              ),
              padding:EdgeInsets.fromLTRB(30, 25, 30, 30)
            ),
            Padding(
              child:RaisedButton(
                onPressed: () async {
                  var latest = await MakeRequest.basicRequest(Query(model: 'restocking', query: 'create'));
                    Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => ProcessRestockingList(query: Query(model: 'restocking', query: latest))),
                  );
                },
                child:Text('Create New Report')
              ),
              padding:EdgeInsets.fromLTRB(30, 0, 0, 0)
            ),
            Padding(
              child:RaisedButton(
                onPressed: () async {
                    var latest = await MakeRequest.basicRequest(Query(model: 'restocking', query: 'latest'));
                    Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => ProcessRestockingList(query: Query(model: 'restocking', query: latest))),
                  );
                },
                child:Text('Latest Report')
              ),
              padding:EdgeInsets.fromLTRB(30, 0, 0, 0)
            )
          ],
        )
      ),
    );
  }
}

class RestockingQuery{
  DateTime time;
  DateTime date;

  RestockingQuery({this.time});
}