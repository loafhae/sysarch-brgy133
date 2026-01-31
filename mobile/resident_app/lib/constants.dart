import 'package:shared_preferences/shared_preferences.dart';

class ApiConstants {
  // Use 127.0.0.1 for Chrome Testing
  static const String baseUrl = "http://127.0.0.1:8000";
}

class StorageService {
  static Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('auth_token', token);
  }

  static Future<void> clear() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }
}