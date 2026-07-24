class AppConfig {

  // ================================
  // 🌐 API CONFIGURATION
  // ================================
  static const String baseUrl = "http://YOUR_SERVER_IP:8000";

  // If using Android Emulator:
  // static const String baseUrl = "http://10.0.2.2:8000";

  // If using physical device:
  // static const String baseUrl = "http://192.168.x.x:8000";


  // ================================
  // 📡 API ENDPOINTS
  // ================================
  static const String dailyCA = "/ca/daily";
  static const String healthCheck = "/health";


  // ================================
  // 🧠 APP SETTINGS
  // ================================
  static const String appName = "UPSC InsightX";

  static const int maxMCQOptions = 4;

  static const int newsCacheLimit = 50;


  // ================================
  // 🎯 FEATURE FLAGS
  // ================================
  static const bool enableOfflineMode = false;
  static const bool enableBookmarks = true;
  static const bool enableDailyQuiz = true;


  // ================================
  // ⏱️ TIME CONFIG
  // ================================
  static const int apiTimeoutSeconds = 15;
}