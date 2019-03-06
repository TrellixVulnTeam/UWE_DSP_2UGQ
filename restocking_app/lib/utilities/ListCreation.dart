import 'package:restocking_app/model/RestockingList.dart';
import 'package:restocking_app/model/Order.dart';

class ListCreation {
  static List<dynamic> createList(var object){
    List<dynamic> toReturn = new List<dynamic>();

    if (object is Order) {
      for (var item in object.orderItems) {
        for(var i = 0; i < item.quantity - item.processed; i++){
          toReturn.add(item);
        }
      }
    }else if(object is RestockingList){
      for (var item in object.restockingListItems) {
        for(var i = 0; i < item.quantity - item.processed; i++){
          toReturn.add(item);
        }
      }
    }
  }
}