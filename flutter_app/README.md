# 🌍 UMAJA KI Agent OS - Flutter App

**Universal Motivation & Joy for All**

> *"The earth is but one country, and mankind its citizens"* — Bahá'u'lláh

A beautiful, multi-platform Flutter application delivering daily inspiration through AI-powered personalities to 8 billion people at zero cost.

---

## 🎯 Mission

UMAJA exists to prove that:
- Technology can serve humanity without profit motive
- AI can bring daily joy to everyone, everywhere
- Global scale is achievable at zero cost
- Spiritual principles translate to beautiful user experiences
- Every person deserves daily inspiration

Built on **Bahá'í principles** of unity, service, and beauty.

---

## ✨ Features

### 🏠 Home Screen
- Daily inspirational content ("Daily Smile")
- Beautiful Material Design 3 interface
- Floating action button to refresh content
- Responsive and accessible design

### 🎭 Personalities Screen
Choose from 3 unique AI comedian personalities:
- **🎩 John Cleese** - British wit and observational comedy
- **🤖 C-3PO** - Protocol-obsessed, analytical humor
- **🎪 Robin Williams** - High-energy, heartfelt inspiration

### ⚙️ Settings Screen
- **Language Selection**: 8 languages supported
  - 🇬🇧 English
  - 🇪🇸 Spanish (Español)
  - 🇮🇳 Hindi (हिन्दी)
  - 🇸🇦 Arabic (العربية)
  - 🇨🇳 Chinese (中文)
  - 🇵🇹 Portuguese (Português)
  - 🇫🇷 French (Français)
  - 🇷🇺 Russian (Русский)
- **Theme Toggle**: Light, Dark, or System Default
- **About Section**: Mission statement and app information

### 🎨 Design Principles
- **Material Design 3** with dynamic color schemes
- **Accessibility-first** with proper contrast and semantic widgets
- **Energy-efficient** with minimal animations
- **Offline-ready** architecture preparation
- **Multi-platform** support (Android, iOS, Web, Desktop)

---

## 🚀 Getting Started

### Prerequisites

- **Flutter SDK**: Version 3.0.0 or higher
  - [Install Flutter](https://docs.flutter.dev/get-started/install)
- **Dart SDK**: Comes with Flutter
- **IDE**: VS Code, Android Studio, or IntelliJ IDEA
  - Recommended: [VS Code with Flutter extension](https://marketplace.visualstudio.com/items?itemName=Dart-Code.flutter)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harrie19/UMAJA-Core.git
   cd UMAJA-Core/flutter_app
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Verify installation**
   ```bash
   flutter doctor
   ```
   Ensure all checks pass (at least one device available).

---

## 📱 Running the App

### Android

#### Emulator
```bash
# Start an Android emulator first, then:
flutter run
```

#### Physical Device
1. Enable Developer Mode and USB Debugging on your device
2. Connect via USB
3. Run:
   ```bash
   flutter devices  # Verify device is detected
   flutter run
   ```

### iOS (macOS only)

#### Simulator
```bash
# Start iOS simulator, then:
flutter run
```

#### Physical Device
1. Connect your iOS device
2. Configure signing in Xcode
3. Run:
   ```bash
   flutter run
   ```

### Web

```bash
flutter run -d chrome
```

Or for other browsers:
```bash
flutter run -d web-server
# Then open http://localhost:port in your browser
```

### Desktop

#### Linux
```bash
flutter run -d linux
```

#### macOS
```bash
flutter run -d macos
```

#### Windows
```bash
flutter run -d windows
```

---

## 🏗️ Project Structure

```
flutter_app/
├── lib/
│   ├── main.dart                    # App entry point & navigation
│   ├── models/
│   │   ├── personality.dart         # Personality model & data
│   │   └── daily_smile.dart         # Daily smile/inspiration model
│   ├── screens/
│   │   ├── home_screen.dart         # Home screen with daily smile
│   │   ├── personalities_screen.dart # Personality selection
│   │   └── settings_screen.dart     # Settings & preferences
│   ├── widgets/
│   │   ├── smile_card.dart          # Daily smile card widget
│   │   └── personality_card.dart    # Personality selection card
│   └── services/
│       └── content_service.dart     # Content management service
├── pubspec.yaml                     # Dependencies & config
└── README.md                        # This file
```

### Key Files

- **`main.dart`**: Application entry point with Material Design 3 theming and bottom navigation
- **Models**: Data structures for personalities and daily smiles
- **Screens**: Three main screens (Home, Personalities, Settings)
- **Widgets**: Reusable UI components
- **Services**: Business logic and data management (placeholder for future API integration)

---

## 🔧 Development

### Code Quality

**Linting**
```bash
flutter analyze
```

**Formatting**
```bash
flutter format .
```

### Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage
```

### Building

**Android APK**
```bash
flutter build apk --release
# Output: build/app/outputs/flutter-apk/app-release.apk
```

**iOS**
```bash
flutter build ios --release
# Requires macOS and Xcode
```

**Web**
```bash
flutter build web --release
# Output: build/web/
```

**Desktop**
```bash
# Linux
flutter build linux --release

# macOS
flutter build macos --release

# Windows
flutter build windows --release
```

---

## 🎨 Customization

### Changing Theme Colors

Edit `lib/main.dart`:
```dart
colorScheme: ColorScheme.fromSeed(
  seedColor: Colors.deepPurple,  // Change this color
  brightness: Brightness.light,
),
```

### Adding New Personalities

Edit `lib/models/personality.dart`:
```dart
Personality(
  id: 'new_personality',
  name: 'Name',
  description: 'Description',
  style: 'Style',
  emoji: '😀',
),
```

### Adding Languages

Edit `lib/services/content_service.dart`:
```dart
Map<String, String> getAvailableLanguages() {
  return {
    'new': 'New Language',
    // ... existing languages
  };
}
```

---

## 🌐 Future Integration

### Backend API Connection

The `ContentService` is currently using placeholder data. To connect to the UMAJA backend:

1. Add HTTP package to `pubspec.yaml`:
   ```yaml
   dependencies:
     http: ^1.1.0
   ```

2. Update `lib/services/content_service.dart`:
   ```dart
   Future<DailySmile> getDailySmile() async {
     final response = await http.get(
       Uri.parse('https://umaja-core-production.up.railway.app/api/daily-smile')
     );
     return DailySmile.fromJson(jsonDecode(response.body));
   }
   ```

### Internationalization (i18n)

For full i18n support:

1. Enable in `pubspec.yaml`:
   ```yaml
   flutter:
     generate: true
   ```

2. Create `l10n.yaml`:
   ```yaml
   arb-dir: lib/l10n
   template-arb-file: app_en.arb
   output-localization-file: app_localizations.dart
   ```

3. Add ARB files for each language in `lib/l10n/`

---

## 📊 Technical Specifications

- **Flutter SDK**: 3.0.0+
- **Dart SDK**: 3.0.0+
- **Material Design**: Version 3
- **State Management**: Provider
- **Storage**: SharedPreferences
- **Architecture**: Clean architecture with separation of concerns

### Dependencies

- `provider: ^6.1.1` - State management
- `shared_preferences: ^2.2.2` - Local storage
- `intl: ^0.19.0` - Internationalization support
- `cupertino_icons: ^1.0.6` - iOS-style icons

---

## 🐛 Troubleshooting

### Flutter doctor issues
```bash
flutter doctor -v
# Follow instructions to resolve issues
```

### Clear build cache
```bash
flutter clean
flutter pub get
```

### Android build fails
```bash
cd android
./gradlew clean
cd ..
flutter build apk
```

### iOS build fails (macOS)
```bash
cd ios
pod install
cd ..
flutter build ios
```

---

## 🤝 Contributing

We welcome contributions! Areas where you can help:

- 🌐 **Translations**: Add support for more languages
- 🎭 **Personalities**: Suggest new AI personalities
- 🎨 **UI/UX**: Improve design and user experience
- 🐛 **Bug Fixes**: Report and fix issues
- 📚 **Documentation**: Improve setup guides and tutorials

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is part of UMAJA-Core and follows the same open-source principles.

---

## 🌍 About UMAJA

**UMAJA** brings personalized daily inspiration to 8 billion people at zero cost.

### Our Reach
- **8 Languages**: Reaching 5.1 billion people (64% of global population)
- **3 Personalities**: Unique AI-powered comedy styles
- **365 Days**: Pre-generated content for infinite scalability
- **$0 Cost**: CDN-based distribution, no servers needed

### Bahá'í Principles

- **Truth**: Transparent about capabilities and limitations
- **Unity**: Serves all 8 billion people equally
- **Service**: Mission-focused, accessible to all
- **Justice**: Equal access worldwide
- **Humility**: Acknowledges limitations, open to improvement

---

## 📞 Contact

- **Email**: Umaja1919@googlemail.com
- **GitHub**: [harrie19/UMAJA-Core](https://github.com/harrie19/UMAJA-Core)
- **Website**: [UMAJA Dashboard](https://harrie19.github.io/UMAJA-Core/)

---

<div align="center">

**🕊️ Built with ❤️ for 8 billion humans 🕊️**

[⭐ Star on GitHub](https://github.com/harrie19/UMAJA-Core) • [🐛 Report Bug](https://github.com/harrie19/UMAJA-Core/issues) • [✨ Request Feature](https://github.com/harrie19/UMAJA-Core/issues)

</div>
