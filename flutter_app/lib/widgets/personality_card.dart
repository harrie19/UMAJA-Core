import 'package:flutter/material.dart';
import '../models/personality.dart';

/// Widget to display a personality card
class PersonalityCard extends StatelessWidget {
  final Personality personality;
  final bool isSelected;
  final VoidCallback onTap;

  const PersonalityCard({
    super.key,
    required this.personality,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Card(
      elevation: isSelected ? 8 : 2,
      color: isSelected 
          ? theme.colorScheme.primaryContainer 
          : theme.colorScheme.surface,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              // Emoji/Avatar
              Container(
                width: 56,
                height: 56,
                decoration: BoxDecoration(
                  color: theme.colorScheme.primary.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(28),
                ),
                child: Center(
                  child: Text(
                    personality.emoji,
                    style: const TextStyle(fontSize: 32),
                  ),
                ),
              ),
              const SizedBox(width: 16),
              
              // Text content
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      personality.name,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: isSelected 
                            ? theme.colorScheme.onPrimaryContainer 
                            : theme.colorScheme.onSurface,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      personality.style,
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: isSelected 
                            ? theme.colorScheme.onPrimaryContainer.withOpacity(0.7) 
                            : theme.colorScheme.secondary,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      personality.description,
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: isSelected 
                            ? theme.colorScheme.onPrimaryContainer.withOpacity(0.8) 
                            : theme.colorScheme.onSurface.withOpacity(0.7),
                      ),
                    ),
                  ],
                ),
              ),
              
              // Selected indicator
              if (isSelected)
                Icon(
                  Icons.check_circle,
                  color: theme.colorScheme.primary,
                  size: 28,
                ),
            ],
          ),
        ),
      ),
    );
  }
}
