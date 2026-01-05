import 'package:flutter/material.dart';
import '../models/daily_smile.dart';
import '../services/content_service.dart';
import '../widgets/smile_card.dart';

/// Home screen showing today's daily smile
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ContentService _contentService = ContentService();
  late Future<DailySmile> _smileFuture;

  @override
  void initState() {
    super.initState();
    _smileFuture = _contentService.getDailySmile();
  }

  void _refreshContent() {
    setState(() {
      _smileFuture = _contentService.refreshContent();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            const Text('🌍 UMAJA'),
            const SizedBox(width: 8),
            Text(
              'KI Agent OS',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: Theme.of(context).colorScheme.primary,
                  ),
            ),
          ],
        ),
        elevation: 2,
      ),
      body: FutureBuilder<DailySmile>(
        future: _smileFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.error_outline,
                    size: 64,
                    color: Colors.red,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Failed to load daily smile',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    snapshot.error.toString(),
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton.icon(
                    onPressed: _refreshContent,
                    icon: const Icon(Icons.refresh),
                    label: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          if (!snapshot.hasData) {
            return const Center(
              child: Text('No content available'),
            );
          }

          return ListView(
            children: [
              SmileCard(
                smile: snapshot.data!,
                onRefresh: _refreshContent,
              ),
              Padding(
                padding: const EdgeInsets.all(16),
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '✨ About UMAJA',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                        const SizedBox(height: 12),
                        Text(
                          'Bringing personalized daily inspiration to 8 billion people at zero cost through:',
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 8),
                        _buildFeature(context, '🎭', '3 AI Personalities'),
                        _buildFeature(context, '🌍', '8 Languages'),
                        _buildFeature(context, '📅', '365 Days of Content'),
                        _buildFeature(context, '💰', 'Zero Cost'),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _refreshContent,
        tooltip: 'Refresh Content',
        child: const Icon(Icons.refresh),
      ),
    );
  }

  Widget _buildFeature(BuildContext context, String emoji, String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Text(emoji, style: const TextStyle(fontSize: 20)),
          const SizedBox(width: 8),
          Text(
            text,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
        ],
      ),
    );
  }
}
