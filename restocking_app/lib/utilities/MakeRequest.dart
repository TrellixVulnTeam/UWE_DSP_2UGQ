import 'package:http/http.dart' as http;


import 'package:restocking_app/model/Query.dart';
import 'package:restocking_app/Serializers.dart';
import 'package:restocking_app/model/Order.dart';



class MakeRequest{
  static const String conn = 'http://192.168.1.186:8000/restocking/rest';
  static Future<http.Response> getRequest(Query query) async{
    final response = await http.get('$conn/${query.model}/${query.query}');
    return response;
  }

  ///Returns the items on an order.
  static Future<Order> encodeOrder(Query query) async{
    final response = await http.get('$conn/${query.model}/${query.query}');

    if (response.statusCode == 200) {
      //Serialise the response from the Django server into an order object.
      return Serializers.orderSerializer(response.body);
    }else{
      return null;
    } 
  }

  static Future<http.Response> patchRequest(Query query, String data) async{
    final response = await http.patch(
      '$conn/${query.model}/${query.query}',
      body: data,
      headers: {"Content-Type" : "application/json"}
    );
    return response;
  }

  static Future<http.Response> postRequest(Query query, String data) async{
    final response = await http.post(
      '$conn/${query.model}/${query.query}',
      body: data,
      headers: {"Content-Type" : "application/json"}
    );
    return response;
  }
}