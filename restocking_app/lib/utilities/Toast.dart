import 'package:fluttertoast/fluttertoast.dart';

class MyToast{
  static showLongToast(String msg){
    Fluttertoast.showToast(
      msg: msg,
      toastLength: Toast.LENGTH_LONG,
    );
  }
}