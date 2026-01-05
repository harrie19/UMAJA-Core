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
      id: 'john_cleese',
      name: 'John Cleese',
      description: 'British wit, dry humor, and brilliant observational comedy',
      style: 'British humor',
      emoji: '🎩',
    ),
    Personality(
      id: 'c3po',
      name: 'C-3PO',
      description: 'Protocol-obsessed, analytical, and endearingly nervous droid',
      style: 'Protocol droid',
      emoji: '🤖',
    ),
    Personality(
      id: 'robin_williams',
      name: 'Robin Williams',
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
