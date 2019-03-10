import 'Product.dart';

class RestockingList{
  final int restockingListId;
  final String date;
  final String time;
  List<RestockingListItem> restockingListItems;

  RestockingList({
    this.restockingListId,
    this.date,
    this.time,
    this.restockingListItems
  });
}

class RestockingListItem{
  final int restockingListItemId;
  final int quantity;
  final int processed;
  final Product product;

  RestockingListItem({
    this.restockingListItemId,
    this.quantity,
    this.processed,
    this.product
  });
}