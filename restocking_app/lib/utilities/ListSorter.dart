import 'package:restocking_app/model/RestockingList.dart';
import 'package:queries/collections.dart';

class ListSorter{
  static RestockingList sortRestockingList(RestockingList lst, String type){
    Collection data = new Collection<RestockingListItem>(lst.restockingListItems);
    switch (type) {
      case 'name':
        lst.restockingListItems.sort((a, b) => a.product.name.compareTo(b.product.name));
        break;
      case 'childrens':
        //Sort by department...
        for (var item in lst.restockingListItems) {
          if (item.product.department == 'childrens') {
            var itm = item;
            lst.restockingListItems.remove(item);
            lst.restockingListItems.insert(0, itm);
          }
        }
        int len = getDepartmentQuantity(lst.restockingListItems, 'childrens');
        //...then code...
        for (var i = 0; i < len - 1; i++) {
          for (var j = 0; j < len - i - 1; j++){
            if (lst.restockingListItems[j].product.productCode.compareTo(lst.restockingListItems[j + 1].product.productCode) == 1) {
              RestockingListItem temp = lst.restockingListItems[j];
              lst.restockingListItems[j] = lst.restockingListItems[j + 1];
              lst.restockingListItems[j + 1] = temp;
            }
          }
        }
        //...then size
        for (var i = 0; i < len - 1; i++) {
          for (var j = 0; j < len - i - 1; j++){
            if (lst.restockingListItems[j].product.size > lst.restockingListItems[j + 1].product.size) {
              RestockingListItem temp = lst.restockingListItems[j];
              lst.restockingListItems[j] = lst.restockingListItems[j + 1];
              lst.restockingListItems[j + 1] = temp;
            }
          }
        }
        break;
      case 'ladies'://By default, sort by Department, then Code, then Size
        //Sort by department...
        for (var item in lst.restockingListItems) {
          if (item.product.department == 'ladies') {
            var itm = item;
            lst.restockingListItems.remove(item);
            lst.restockingListItems.insert(0, itm);
          }
        }
        int len = getDepartmentQuantity(lst.restockingListItems, 'ladies');
        //...then code...
        for (var i = 0; i < len - 1; i++) {
          for (var j = 0; j < len - i - 1; j++){
            if (lst.restockingListItems[j].product.productCode.compareTo(lst.restockingListItems[j + 1].product.productCode) == 1) {
              RestockingListItem temp = lst.restockingListItems[j];
              lst.restockingListItems[j] = lst.restockingListItems[j + 1];
              lst.restockingListItems[j + 1] = temp;
            }
          }
        }
        //...then size
        for (var i = 0; i < len - 1; i++) {
          for (var j = 0; j < len - i - 1; j++){
            if (lst.restockingListItems[j].product.size > lst.restockingListItems[j + 1].product.size) {
              RestockingListItem temp = lst.restockingListItems[j];
              lst.restockingListItems[j] = lst.restockingListItems[j + 1];
              lst.restockingListItems[j + 1] = temp;
            }
          }
        }
        break;
      case 'mens':
        //Sort by department...
        for (var item in lst.restockingListItems) {
          if (item.product.department == 'mens') {
            var itm = item;
            lst.restockingListItems.remove(item);
            lst.restockingListItems.insert(0, itm);
          }
        }
        int len = getDepartmentQuantity(lst.restockingListItems, 'mens');
        //...then code...
        for (var i = 0; i < len - 1; i++) {
          for (var j = 0; j < len - i - 1; j++){
            if (lst.restockingListItems[j].product.productCode.compareTo(lst.restockingListItems[j + 1].product.productCode) == 1) {
              RestockingListItem temp = lst.restockingListItems[j];
              lst.restockingListItems[j] = lst.restockingListItems[j + 1];
              lst.restockingListItems[j + 1] = temp;
            }
          }
        }
        //...then size
        for (var i = 0; i < len - 1; i++) {
          for (var j = 0; j < len - i - 1; j++){
            if (lst.restockingListItems[j].product.size > lst.restockingListItems[j + 1].product.size) {
              RestockingListItem temp = lst.restockingListItems[j];
              lst.restockingListItems[j] = lst.restockingListItems[j + 1];
              lst.restockingListItems[j + 1] = temp;
            }
          }
        }
        break;
      case 'size':
        lst.restockingListItems.sort((a, b) => a.product.size.compareTo(b.product.size));
        break;
    }

    lst.restockingListItems = data.toList();
    return lst;
  }

  static int getDepartmentQuantity(List<dynamic> list, String param){
    int quantity = 0;
    for (var item in list) {
      if (item.product.department == param) {
        quantity++;
      }
    }
    return quantity;
  }
}