import 'package:flutter/material.dart';
import '../models/personality.dart';
import '../services/content_service.dart';
import '../widgets/personality_card.dart';

/// Screen displaying available comedian personalities
class PersonalitiesScreen extends StatefulWidget {
  const PersonalitiesScreen({super.key});

  @override
  State<PersonalitiesScreen> createState() => _PersonalitiesScreenState();
}

class _PersonalitiesScreenState extends State<PersonalitiesScreen> {
  final ContentService _contentService = ContentService();
  late String _selectedPersonalityId;

  @override
  void initState() {
    super.initState();
    _selectedPersonalityId = _contentService.selectedPersonalityId;
  }

  void _selectPersonality(String personalityId) {
    setState(() {
      _selectedPersonalityId = personalityId;
      _contentService.setPersonality(personalityId);
    });

    // Show confirmation
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          'Selected ${Personality.getById(personalityId)?.name ?? "personality"}',
        ),
        duration: const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final personalities = _contentService.getPersonalities();

    return Scaffold(
      appBar: AppBar(
        title: const Text('🎭 Personalities'),
        elevation: 2,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Header
          Text(
            'Choose Your Comedy Style',
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
          ),
          const SizedBox(height: 8),
          Text(
            'Select a personality to customize your daily inspiration',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                ),
          ),
          const SizedBox(height: 24),

          // Personality cards
          ...personalities.map((personality) {
            return Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: PersonalityCard(
                personality: personality,
                isSelected: personality.id == _selectedPersonalityId,
                onTap: () => _selectPersonality(personality.id),
              ),
            );
          }),

          const SizedBox(height: 16),

          // Info card
          Card(
            color: Theme.of(context).colorScheme.primaryContainer.withOpacity(0.3),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        Icons.info_outline,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'About Personalities',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.bold,
                            ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Each personality brings unique style and energy to your daily inspiration. '
                    'All content is AI-powered and carefully crafted to bring joy while respecting '
                    'Bahá\'í principles of unity, service, and beauty.',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
