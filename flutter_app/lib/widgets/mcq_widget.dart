import 'package:flutter/material.dart';
import '../models/current_affairs_model.dart';

class McqWidget extends StatefulWidget {
  final McqModel mcq;

  const McqWidget({
    super.key,
    required this.mcq,
  });

  @override
  State<McqWidget> createState() => _McqWidgetState();
}

class _McqWidgetState extends State<McqWidget> {

  String? selectedOption;
  bool checked = false;

  void checkAnswer() {
    setState(() {
      checked = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      elevation: 3,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            // QUESTION
            Text(
              widget.mcq.question,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 10),

            // OPTIONS
            ...widget.mcq.options.map((option) {
              return RadioListTile<String>(
                title: Text(option),
                value: option,
                groupValue: selectedOption,
                onChanged: checked
                    ? null
                    : (value) {
                        setState(() {
                          selectedOption = value;
                        });
                      },
              );
            }),

            const SizedBox(height: 10),

            // BUTTON
            ElevatedButton(
              onPressed: selectedOption == null ? null : checkAnswer,
              child: const Text("Check Answer"),
            ),

            const SizedBox(height: 10),

            // RESULT
            if (checked)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: selectedOption == widget.mcq.answer
                      ? Colors.green.shade100
                      : Colors.red.shade100,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  selectedOption == widget.mcq.answer
                      ? "✅ Correct Answer"
                      : "❌ Wrong! Correct: ${widget.mcq.answer}",
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ),
          ],
        ),
      ),
    );
  }
}