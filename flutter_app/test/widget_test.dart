import 'package:flutter_test/flutter_test.dart';
import 'package:umaja_ki_agent/main.dart';

void main() {
  testWidgets('App launches and displays Home screen', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const UmajaApp());

    // Verify that the app bar shows UMAJA branding
    expect(find.text('🌍 UMAJA'), findsOneWidget);
    
    // Verify bottom navigation is present
    expect(find.text('Home'), findsOneWidget);
    expect(find.text('Personalities'), findsOneWidget);
    expect(find.text('Settings'), findsOneWidget);
  });
}
