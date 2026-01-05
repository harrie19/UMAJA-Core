/// Model representing a daily smile/inspiration
class DailySmile {
  final String content;
  final String personalityId;
  final DateTime date;
  final String? language;

  const DailySmile({
    required this.content,
    required this.personalityId,
    required this.date,
    this.language = 'en',
  });

  /// Create a placeholder smile
  factory DailySmile.placeholder() {
    return DailySmile(
      content: '🌍 "The earth is but one country, and mankind its citizens."\n\n'
          'Welcome to UMAJA - your daily source of inspiration bringing joy to 8 billion people worldwide!\n\n'
          'Each day, discover personalized motivation delivered through unique AI personalities, '
          'available in 8 languages, at zero cost. Built on Bahá\'í principles of unity, service, and beauty.',
      personalityId: 'john_cleese',
      date: DateTime.now(),
      language: 'en',
    );
  }

  /// Create from JSON
  factory DailySmile.fromJson(Map<String, dynamic> json) {
    return DailySmile(
      content: json['content'] as String,
      personalityId: json['personalityId'] as String,
      date: DateTime.parse(json['date'] as String),
      language: json['language'] as String? ?? 'en',
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'content': content,
      'personalityId': personalityId,
      'date': date.toIso8601String(),
      'language': language,
    };
  }
}
