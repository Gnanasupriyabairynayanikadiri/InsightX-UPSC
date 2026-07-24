import 'package:flutter/material.dart';
import 'current_affairs_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("🧠 UPSC Insight App"),
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            const Text(
              "Welcome to UPSC Current Affairs Hub",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 20),

            _buildCard(
              context,
              title: "📰 Current Affairs",
              subtitle: "Daily UPSC News + MCQs + Mains",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const CurrentAffairsScreen(),
                  ),
                );
              },
            ),

            const SizedBox(height: 12),

            _buildCard(
              context,
              title: "📚 Revision (Coming Soon)",
              subtitle: "Smart revision system",
              onTap: () {},
            ),

            const SizedBox(height: 12),

            _buildCard(
              context,
              title: "🧠 Mock Tests (Coming Soon)",
              subtitle: "Full UPSC test engine",
              onTap: () {},
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCard(
    BuildContext context, {
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 3,
      child: ListTile(
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.arrow_forward_ios),
        onTap: onTap,
      ),
    );
  }
}