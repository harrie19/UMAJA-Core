import 'package:flutter/material.dart';
import '../models/daily_smile.dart';
import '../models/personality.dart';

/// Widget to display a daily smile/inspiration card
class SmileCard extends StatelessWidget {
  final DailySmile smile;
  final VoidCallback? onRefresh;

  const SmileCard({
    super.key,
    required this.smile,
    this.onRefresh,
  });

  @override
  Widget build(BuildContext context) {
    final personality = Personality.getById(smile.personalityId);
    final theme = Theme.of(context);

    return Card(
      elevation: 4,
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header with personality info
            Row(
              children: [
                Text(
                  personality?.emoji ?? '✨',
                  style: const TextStyle(fontSize: 32),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Today\'s Daily Smile',
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (personality != null)
                        Text(
                          'by ${personality.name}',
                          style: theme.textTheme.bodySmall?.copyWith(
                            color: theme.colorScheme.secondary,
                          ),
                        ),
                    ],
                  ),
                ),
              ],
            ),
            const Divider(height: 24),
            
            // Content
            Text(
              smile.content,
              style: theme.textTheme.bodyLarge?.copyWith(
                height: 1.6,
              ),
            ),
            
            const SizedBox(height: 16),
            
            // Footer with date
            Text(
              '${smile.date.day}/${smile.date.month}/${smile.date.year}',
              style: theme.textTheme.bodySmall?.copyWith(
                color: theme.colorScheme.outline,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
