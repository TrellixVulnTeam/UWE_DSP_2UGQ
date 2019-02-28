import 'package:flutter/material.dart';

class ColorResolver{
  static Color colorResolver(String color){
    switch (color) {
      case 'Navy':
        return Color.fromRGBO(0, 0, 128, 100);
        break;
      case 'Brown':
        return Colors.brown;
        break;
      case 'White':
        return Colors.grey;
        break;
      case 'Black':
        return Colors.black;
      default:
        return Colors.white;
    }
  }
}