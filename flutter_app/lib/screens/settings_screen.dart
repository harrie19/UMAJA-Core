import 'package:flutter/material.dart';
import '../services/content_service.dart';

/// Settings screen with language selector, theme toggle, and about section
class SettingsScreen extends StatefulWidget {
  final Function(ThemeMode) onThemeChanged;
  final ThemeMode currentTheme;

  const SettingsScreen({
    super.key,
    required this.onThemeChanged,
    required this.currentTheme,
  });

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final ContentService _contentService = ContentService();
  late String _selectedLanguage;

  @override
  void initState() {
    super.initState();
    _selectedLanguage = _contentService.selectedLanguage;
  }

  void _selectLanguage(String languageCode) {
    setState(() {
      _selectedLanguage = languageCode;
      _contentService.setLanguage(languageCode);
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Language set to ${_contentService.getAvailableLanguages()[languageCode]}'),
        duration: const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final availableLanguages = _contentService.getAvailableLanguages();
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('⚙️ Settings'),
        elevation: 2,
      ),
      body: ListView(
        children: [
          // Language Section
          _buildSectionHeader(context, 'Language'),
          Card(
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Column(
              children: availableLanguages.entries.map((entry) {
                final isSelected = entry.key == _selectedLanguage;
                return ListTile(
                  leading: Text(
                    _getLanguageEmoji(entry.key),
                    style: const TextStyle(fontSize: 24),
                  ),
                  title: Text(entry.value),
                  subtitle: Text(entry.key.toUpperCase()),
                  trailing: isSelected
                      ? Icon(
                          Icons.check_circle,
                          color: theme.colorScheme.primary,
                        )
                      : null,
                  selected: isSelected,
                  onTap: () => _selectLanguage(entry.key),
                );
              }).toList(),
            ),
          ),

          // Theme Section
          const SizedBox(height: 24),
          _buildSectionHeader(context, 'Appearance'),
          Card(
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Column(
              children: [
                RadioListTile<ThemeMode>(
                  title: const Text('Light Theme'),
                  subtitle: const Text('Bright and vibrant'),
                  value: ThemeMode.light,
                  groupValue: widget.currentTheme,
                  onChanged: (ThemeMode? value) {
                    if (value != null) {
                      widget.onThemeChanged(value);
                    }
                  },
                  secondary: const Icon(Icons.light_mode),
                ),
                RadioListTile<ThemeMode>(
                  title: const Text('Dark Theme'),
                  subtitle: const Text('Easy on the eyes'),
                  value: ThemeMode.dark,
                  groupValue: widget.currentTheme,
                  onChanged: (ThemeMode? value) {
                    if (value != null) {
                      widget.onThemeChanged(value);
                    }
                  },
                  secondary: const Icon(Icons.dark_mode),
                ),
                RadioListTile<ThemeMode>(
                  title: const Text('System Default'),
                  subtitle: const Text('Follow system settings'),
                  value: ThemeMode.system,
                  groupValue: widget.currentTheme,
                  onChanged: (ThemeMode? value) {
                    if (value != null) {
                      widget.onThemeChanged(value);
                    }
                  },
                  secondary: const Icon(Icons.brightness_auto),
                ),
              ],
            ),
          ),

          // About Section
          const SizedBox(height: 24),
          _buildSectionHeader(context, 'About UMAJA'),
          Card(
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Center(
                    child: Text(
                      '🌍 UMAJA KI Agent OS',
                      style: theme.textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Center(
                    child: Text(
                      'Version 1.0.0',
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: theme.colorScheme.outline,
                      ),
                    ),
                  ),
                  const Divider(height: 32),
                  Text(
                    'Mission Statement',
                    style: theme.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '"The earth is but one country, and mankind its citizens"',
                    style: theme.textTheme.bodyMedium?.copyWith(
                      fontStyle: FontStyle.italic,
                      color: theme.colorScheme.primary,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '— Bahá\'u\'lláh',
                    style: theme.textTheme.bodySmall?.copyWith(
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'UMAJA brings personalized daily inspiration to 8 billion people at zero cost. '
                    'Built on Bahá\'í principles of unity, service, and beauty, we deliver joy '
                    'through AI-powered personalities in 8 languages worldwide.',
                    style: theme.textTheme.bodyMedium,
                  ),
                  const SizedBox(height: 16),
                  _buildAboutItem(context, 'Reach', '8 Billion People'),
                  _buildAboutItem(context, 'Languages', '8 Languages'),
                  _buildAboutItem(context, 'Cost', '\$0 - Free Forever'),
                  _buildAboutItem(context, 'Principles', 'Unity, Service, Beauty'),
                  const SizedBox(height: 16),
                  Center(
                    child: Text(
                      '🕊️ Built with ❤️ for humanity 🕊️',
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: theme.colorScheme.outline,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.primary,
            ),
      ),
    );
  }

  Widget _buildAboutItem(BuildContext context, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              label,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ),
        ],
      ),
    );
  }

  String _getLanguageEmoji(String languageCode) {
    const emojiMap = {
      'en': '🇬🇧',
      'es': '🇪🇸',
      'hi': '🇮🇳',
      'ar': '🇸🇦',
      'zh': '🇨🇳',
      'pt': '🇵🇹',
      'fr': '🇫🇷',
      'ru': '🇷🇺',
    };
    return emojiMap[languageCode] ?? '🌍';
  }
}
