/// Model representing a comedian personality in UMAJA
class Personality {
  final String id;
  final String name;
  final String description;
  final String style;
  final String emoji;

  const Personality({
    required this.id,
    required this.name,
    required this.description,
    required this.style,
    required this.emoji,
  });

  /// Predefined comedian personalities
  static const List<Personality> personalities = [
    Personality(
      id: 'distinguished_wit',
      name: 'The Distinguished Wit',
      description: 'British wit, dry humor, and brilliant observational comedy',
      style: 'British humor',
      emoji: '🎩',
    ),
    Personality(
      id: 'anxious_analyzer',
      name: 'The Anxious Analyzer',
      description: 'Protocol-obsessed, analytical, and endearingly nervous',
      style: 'Analytical protocol',
      emoji: '🤖',
    ),
    Personality(
      id: 'energetic_improviser',
      name: 'The Energetic Improviser',
      description: 'High-energy improvisation with heartfelt, inspiring moments',
      style: 'Energetic improviser',
      emoji: '🎪',
    ),
  ];

  /// Get personality by ID
  static Personality? getById(String id) {
    try {
      return personalities.firstWhere((p) => p.id == id);
    } catch (e) {
      return null;
    }
  }
}
