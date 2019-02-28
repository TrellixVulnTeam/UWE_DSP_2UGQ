import 'package:qr_reader/qr_reader.dart';

class Scan {
  static Future<String> scan() async{
    return await QRCodeReader().scan();
  }
}