import 'package:flutter/material.dart';
import 'services/api_service.dart';

void main() {
  runApp(const UPSCApp());
}

class UPSCApp extends StatelessWidget {
  const UPSCApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'UPSC Insight App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  late Future<List<dynamic>> futureNews;

  @override
  void initState() {
    super.initState();
    futureNews = ApiService.fetchDailyCA();
  }

  void refreshData() {
    setState(() {
      futureNews = ApiService.fetchDailyCA();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("📰 UPSC Current Affairs"),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: refreshData,
          )
        ],
      ),

      body: FutureBuilder<List<dynamic>>(
        future: futureNews,
        builder: (context, snapshot) {

          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(
              child: Text(
                "Error: ${snapshot.error}",
                textAlign: TextAlign.center,
              ),
            );
          }

          final newsList = snapshot.data ?? [];

          if (newsList.isEmpty) {
            return const Center(
              child: Text("No Current Affairs Found"),
            );
          }

          return ListView.builder(
            itemCount: newsList.length,
            itemBuilder: (context, index) {

              final item = newsList[index];

              return Card(
                margin: const EdgeInsets.all(10),
                elevation: 3,
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [

                      Text(
                        item["title"] ?? "No Title",
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),

                      const SizedBox(height: 6),

                      Text(
                        "📚 Category: ${item["category"] ?? "N/A"}",
                      ),

                      Text(
                        "🔥 Importance: ${item["importance"] ?? "Medium"}",
                      ),

                      const SizedBox(height: 10),

                      Text(
                        item["description"] ?? "No description available",
                      ),

                      const SizedBox(height: 10),

                      if (item["mains_question"] != null)
                        Container(
                          padding: const EdgeInsets.all(8),
                          color: Colors.blue.shade50,
                          child: Text(
                            "✍️ Mains: ${item["mains_question"]}",
                          ),
                        ),

                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}