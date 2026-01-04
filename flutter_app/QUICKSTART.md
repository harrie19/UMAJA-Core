# 🚀 UMAJA Flutter App - Quick Start Guide

Get the UMAJA KI Agent OS app running in 5 minutes!

## ⚡ Super Quick Start

```bash
# 1. Navigate to the Flutter app
cd flutter_app

# 2. Get dependencies
flutter pub get

# 3. Run the app
flutter run
```

That's it! The app should launch on your connected device or emulator.

---

## 📋 Prerequisites Checklist

Before you start, ensure you have:

- [ ] **Flutter SDK** installed (version 3.0.0+)
  - Check: `flutter --version`
  - Install: https://docs.flutter.dev/get-started/install

- [ ] **At least one device** available:
  - [ ] Android emulator running, OR
  - [ ] iOS simulator running (macOS only), OR
  - [ ] Physical device connected, OR
  - [ ] Web browser (Chrome)

- [ ] **IDE** (optional but recommended):
  - [ ] VS Code with Flutter extension, OR
  - [ ] Android Studio with Flutter plugin

---

## 🎯 Choose Your Platform

### 📱 Android

**Option A: Emulator**
```bash
# Start emulator from Android Studio, then:
flutter run
```

**Option B: Physical Device**
1. Enable Developer Options on your Android device
2. Enable USB Debugging
3. Connect via USB
4. Run: `flutter run`

### 🍎 iOS (macOS only)

**Option A: Simulator**
```bash
# Start simulator, then:
flutter run
```

**Option B: Physical Device**
1. Connect your iPhone/iPad
2. Configure signing in Xcode
3. Run: `flutter run`

### 🌐 Web

```bash
flutter run -d chrome
```

### 💻 Desktop

**Linux**:
```bash
flutter run -d linux
```

**macOS**:
```bash
flutter run -d macos
```

**Windows**:
```bash
flutter run -d windows
```

---

## 🔍 Troubleshooting

### "flutter: command not found"
Flutter is not in your PATH. Add it:

```bash
# Linux/macOS
export PATH="$PATH:/path/to/flutter/bin"

# Add to ~/.bashrc or ~/.zshrc for persistence
```

### "No devices found"
```bash
# Check connected devices
flutter devices

# For Android: Start an emulator
# For iOS: Open simulator
# For Web: Use -d chrome
```

### "Gradle build failed" (Android)
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

### Build errors after git pull
```bash
flutter clean
flutter pub get
```

---

## 🎨 Development Tips

### Hot Reload
While app is running:
- Press `r` to hot reload
- Press `R` to hot restart
- Press `q` to quit

### Debug Mode
The app runs in debug mode by default. You'll see:
- Debug banner in top-right corner
- Slower performance (expected)
- Hot reload capability

### Release Build
For better performance:
```bash
flutter run --release
```

### Format Code
```bash
flutter format .
```

### Analyze Code
```bash
flutter analyze
```

---

## 📸 See It In Action

Once running, you should see:

1. **Home Screen**
   - UMAJA branding in AppBar
   - Daily smile card with inspirational content
   - Floating refresh button
   - Bottom navigation (Home, Personalities, Settings)

2. **Personalities Screen**
   - 3 personality cards:
     - 🎩 John Cleese
     - 🤖 C-3PO
     - 🎪 Robin Williams
   - Tap to select

3. **Settings Screen**
   - 8 language options
   - Theme toggle (Light/Dark/System)
   - About section with mission

---

## 🏗️ Project Structure

```
flutter_app/
├── lib/
│   ├── main.dart              # Start here
│   ├── screens/               # UI screens
│   ├── widgets/               # Reusable components
│   ├── models/                # Data models
│   └── services/              # Business logic
├── test/                      # Tests
└── pubspec.yaml              # Dependencies
```

---

## 🛠️ Common Commands

```bash
# Get dependencies
flutter pub get

# Run app
flutter run

# Run specific device
flutter run -d <device-id>

# List devices
flutter devices

# Build APK (Android)
flutter build apk

# Build for web
flutter build web

# Run tests
flutter test

# Clean build artifacts
flutter clean

# Check Flutter installation
flutter doctor

# Upgrade Flutter
flutter upgrade
```

---

## 📚 Next Steps

1. **Explore the Code**
   - Start with `lib/main.dart`
   - Check out screens in `lib/screens/`
   - Review models in `lib/models/`

2. **Make Changes**
   - Edit a screen
   - Save the file
   - Press `r` for hot reload
   - See changes instantly!

3. **Read Documentation**
   - See `README.md` for full documentation
   - Check `STRUCTURE.md` for architecture details

4. **Run Tests**
   ```bash
   flutter test
   ```

5. **Build for Production**
   ```bash
   flutter build apk --release
   ```

---

## 🆘 Need Help?

- **Flutter Docs**: https://docs.flutter.dev
- **UMAJA Repository**: https://github.com/harrie19/UMAJA-Core
- **Issue Tracker**: https://github.com/harrie19/UMAJA-Core/issues
- **Email**: Umaja1919@googlemail.com

---

## ✅ Success Checklist

- [ ] Flutter SDK installed and in PATH
- [ ] `flutter doctor` shows no critical issues
- [ ] Can see at least one device with `flutter devices`
- [ ] Successfully ran `flutter pub get`
- [ ] App launches with `flutter run`
- [ ] Can navigate between all 3 screens
- [ ] Can select different personalities
- [ ] Can change theme and language
- [ ] Hot reload works (press `r` after code change)

---

## 🎉 You're All Set!

Welcome to UMAJA KI Agent OS development! You're now ready to:
- Explore the beautiful Material Design 3 interface
- Customize personalities and content
- Build for multiple platforms
- Contribute to bringing joy to 8 billion people

**Remember**: Built with ❤️ following Bahá'í principles of unity, service, and beauty.

🌍 Let's bring daily inspiration to the world! 🕊️
