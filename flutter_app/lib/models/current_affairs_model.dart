class CurrentAffairsModel {

  final String title;
  final String description;
  final String source;
  final String link;

  final String category;
  final String importance;
  final double relevanceScore;

  final String quickSummary;
  final String background;
  final String mainsQuestion;

  final List<String> prelimsFocus;
  final List<String> tags;

  final List<McqModel> mcqs;

  CurrentAffairsModel({
    required this.title,
    required this.description,
    required this.source,
    required this.link,
    required this.category,
    required this.importance,
    required this.relevanceScore,
    required this.quickSummary,
    required this.background,
    required this.mainsQuestion,
    required this.prelimsFocus,
    required this.tags,
    required this.mcqs,
  });

  factory CurrentAffairsModel.fromJson(Map<String, dynamic> json) {

    return CurrentAffairsModel(

      title: json["title"] ?? "",
      description: json["description"] ?? "",
      source: json["source"] ?? "",
      link: json["link"] ?? "",

      category: json["category"] ?? "General",
      importance: json["importance"] ?? "Medium",
      relevanceScore: (json["relevance_score"] ?? 0).toDouble(),

      quickSummary: json["quick_summary"] ?? "",
      background: json["background"] ?? "",
      mainsQuestion: json["mains_question"] ?? "",

      prelimsFocus: List<String>.from(
        json["prelims_focus"] ?? []
      ),

      tags: List<String>.from(
        json["tags"] ?? []
      ),

      mcqs: (json["mcqs"] as List? ?? [])
          .map((e) => McqModel.fromJson(e))
          .toList(),
    );
  }
}

class McqModel {

  final String question;
  final List<String> options;
  final String answer;

  McqModel({
    required this.question,
    required this.options,
    required this.answer,
  });

  factory McqModel.fromJson(Map<String, dynamic> json) {

    return McqModel(

      question: json["question"] ?? "",

      options: List<String>.from(
        json["options"] ?? []
      ),

      answer: json["answer"] ?? "",
    );
  }
}