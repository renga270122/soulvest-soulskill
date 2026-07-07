# Installation & Setup Guide for SoulSkill Android App

## Prerequisites

- **Flutter SDK** 3.10+
- **Android SDK** API level 21+
- **Android Studio** or VS Code with Flutter extension
- **Git**

## Quick Start

### 1. Install Flutter

```bash
# Download Flutter from: https://flutter.dev/docs/get-started/install

# Add Flutter to PATH (Windows):
# C:\src\flutter\bin

# Verify installation
flutter doctor
```

### 2. Clone & Setup Project

```bash
cd soulskill_mobile
flutter pub get
```

### 3. Run the App (Emulator or Device)

```bash
# List available devices
flutter devices

# Run on emulator
flutter run

# Run on connected device
flutter run -d <device-id>
```

## Backend Setup

### 1. Install Python Dependencies

```bash
pip install fastapi uvicorn
pip install -r requirements.txt
```

### 2. Run API Server

```bash
python api_server.py
```

The API will run on `http://localhost:8000`

### 3. Connect Mobile App to Backend

**For Emulator:**
- API base URL is already set to `http://10.0.2.2:8000` (Android emulator localhost)

**For Physical Device:**
- Edit `lib/services/api_client.dart`
- Change `baseUrl` to your computer's IP:
  ```dart
  static const String baseUrl = 'http://192.168.1.100:8000';
  ```
- Ensure device is on same WiFi network

## Building APK for Distribution

### Debug APK (Testing)

```bash
flutter build apk --debug
# Output: build/app/outputs/flutter-apk/app-debug.apk
```

### Release APK (Production)

#### 1. Create Keystore (One time)

```bash
keytool -genkey -v -keystore release.jks -keyalg RSA -keysize 2048 -validity 10000 -alias soulskill
```

#### 2. Create `android/key.properties`

```properties
storePassword=<your-password>
keyPassword=<your-password>
keyAlias=soulskill
storeFile=../release.jks
```

#### 3. Build Release APK

```bash
flutter build apk --release
# Output: build/app/outputs/flutter-apk/app-release.apk
```

### Build App Bundle (Google Play)

```bash
flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab
```

## Project Structure

```
soulskill_mobile/
├── lib/
│   ├── main.dart                 # App entry point
│   ├── theme.dart               # Theme & colors
│   ├── screens/
│   │   ├── home_page.dart       # Home screen
│   │   ├── resume_form_page.dart # Resume builder
│   │   └── ats_check_page.dart   # ATS optimizer
│   ├── services/
│   │   └── api_client.dart      # API integration
│   └── providers/
│       └── resume_provider.dart  # State management
├── android/
│   └── app/src/main/AndroidManifest.xml
├── pubspec.yaml                  # Dependencies
└── README.md
```

## Important Notes

- **Default API Port**: 8000
- **Minimum Android API**: 21 (Android 5.0)
- **Target Android API**: 34
- **App Size**: ~50-60 MB (Release APK)
- **Min Storage Required**: 100 MB

## Troubleshooting

### "Cannot connect to API"
- Ensure backend is running: `python api_server.py`
- Check emulator has internet: `flutter run -v`
- For device, verify WiFi and correct IP in `api_client.dart`

### "Missing Flutter SDK"
- Run `flutter doctor` to diagnose
- Follow suggestions for missing tools

### "Build fails"
- Run `flutter clean`
- Run `flutter pub get`
- Run `flutter run`

## Next Steps

1. ✅ Test app locally with emulator
2. ✅ Test with physical device
3. ✅ Deploy to Google Play Store
4. ✅ Deploy backend to production server

## Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Android Development Guide](https://developer.android.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
