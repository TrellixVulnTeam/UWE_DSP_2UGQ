import 'package:flutter/material.dart';

class ColorResolver{
  static Color colorResolver(String color){
    switch (color) {
      case 'Navy':
        return Color.fromRGBO(0, 0, 128, 100);
        break;
      case 'Navy Patent':
        return Color.fromRGBO(0, 0, 128, 100);
        break;
      case 'Brown':
        return Colors.brown;
        break;
      case 'White':
        return Colors.grey;
        break;
      case 'Grey':
        return Colors.blueGrey;
      case 'Black':
        return Colors.black;
      case 'Black Patent':
        return Colors.black12;
      case 'Red':
        return Colors.red;
      case 'Purple':
        return Colors.purple;
      case 'Pink':
        return Colors.pink;
      case 'Gold':
        return Colors.yellow;
      case 'Multi':
        return Colors.grey;
      case 'Tan':
        return Color.fromRGBO(210, 180, 140, 100);
      case 'Green':
        return Colors.green;
      case 'Blue':
        return Colors.blue;
      case 'Silver':
        return Colors.grey;
      default:
        return Colors.white;
    }
  }
}