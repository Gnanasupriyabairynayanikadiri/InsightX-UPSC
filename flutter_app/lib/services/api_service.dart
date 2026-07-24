import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {

  static const String baseUrl = "http://10.0.2.2:8000"; // Android emulator

  static Future<List<dynamic>> fetchDailyCA() async {
    final response = await http.get(
      Uri.parse("$baseUrl/ca/daily"),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data["data"];
    } else {
      throw Exception("Failed to load current affairs");
    }
  }
}