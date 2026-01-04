import '../models/daily_smile.dart';
import '../models/personality.dart';

/// Service for managing content (smiles, personalities)
/// This is a placeholder - will be connected to UMAJA backend API later
class ContentService {
  // Singleton pattern
  static final ContentService _instance = ContentService._internal();
  factory ContentService() => _instance;
  ContentService._internal();

  String _selectedPersonalityId = 'john_cleese';
  String _selectedLanguage = 'en';

  /// Get the selected personality
  String get selectedPersonalityId => _selectedPersonalityId;

  /// Set the selected personality
  void setPersonality(String personalityId) {
    _selectedPersonalityId = personalityId;
  }

  /// Get the selected language
  String get selectedLanguage => _selectedLanguage;

  /// Set the selected language
  void setLanguage(String language) {
    _selectedLanguage = language;
  }

  /// Fetch today's daily smile
  /// TODO: Connect to UMAJA backend API
  Future<DailySmile> getDailySmile() async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 500));
    
    // Return placeholder for now
    return DailySmile.placeholder();
  }

  /// Refresh content
  Future<DailySmile> refreshContent() async {
    // In future, this will fetch new content from the API
    return getDailySmile();
  }

  /// Get all available personalities
  List<Personality> getPersonalities() {
    return Personality.personalities;
  }

  /// Get available languages with their native names
  Map<String, String> getAvailableLanguages() {
    return {
      'en': 'English',
      'es': 'Español',
      'hi': 'हिन्दी',
      'ar': 'العربية',
      'zh': '中文',
      'pt': 'Português',
      'fr': 'Français',
      'ru': 'Русский',
    };
  }
}
