import 'package:flutter/material.dart';

class MyDialog{
  static AlertDialog showAlertDialog(String title, String content, BuildContext context){
    return AlertDialog(
      title: Text(title),
      content: Text(content),
      actions: <Widget>[
        new RaisedButton(
          child: Text('Okay'),
          onPressed: (){
            Navigator.of(context).pop();
          },
        )
      ],
    );
  }
}