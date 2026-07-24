import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/current_affairs_model.dart';

class CurrentAffairsScreen extends StatefulWidget {
  const CurrentAffairsScreen({super.key});

  @override
  State<CurrentAffairsScreen> createState() => _CurrentAffairsScreenState();
}

class _CurrentAffairsScreenState extends State<CurrentAffairsScreen> {

  late Future<List<dynamic>> futureData;

  @override
  void initState() {
    super.initState();
    futureData = ApiService.fetchDailyCA();
  }

  void refresh() {
    setState(() {
      futureData = ApiService.fetchDailyCA();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("📰 Current Affairs"),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: refresh,
          )
        ],
      ),

      body: FutureBuilder<List<dynamic>>(
        future: futureData,
        builder: (context, snapshot) {

          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(
              child: Text("Error: ${snapshot.error}"),
            );
          }

          final rawList = snapshot.data ?? [];

          if (rawList.isEmpty) {
            return const Center(child: Text("No data available"));
          }

          // convert JSON → Model
          final newsList = rawList
              .map((e) => CurrentAffairsModel.fromJson(e))
              .toList();

          return ListView.builder(
            itemCount: newsList.length,
            itemBuilder: (context, index) {

              final item = newsList[index];

              return Card(
                margin: const EdgeInsets.all(10),
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [

                      Text(
                        item.title,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),

                      const SizedBox(height: 6),

                      Text("📚 ${item.category} | 🔥 ${item.importance}"),

                      const SizedBox(height: 10),

                      Text(item.quickSummary),

                      const SizedBox(height: 10),

                      if (item.mainsQuestion.isNotEmpty)
                        Container(
                          padding: const EdgeInsets.all(8),
                          color: Colors.blue.shade50,
                          child: Text("✍️ ${item.mainsQuestion}"),
                        ),

                      const SizedBox(height: 10),

                      ExpansionTile(
                        title: const Text("🧠 MCQs"),
                        children: item.mcqs.map((mcq) {

                          return ListTile(
                            title: Text(mcq.question),
                            subtitle: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: mcq.options
                                  .map((opt) => Text("• $opt"))
                                  .toList(),
                            ),
                          );

                        }).toList(),
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