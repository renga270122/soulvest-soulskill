# SoulSkill Android App

A modern, Android-first resume studio built with Flutter. This mobile client is being reconstructed because the previous Flutter application source and Android host project are not present in the tracked repository.

## Current MVP

- Modern home dashboard with resume-completion progress.
- Structured resume editor for contact details, professional summary, work experience, education and skills.
- Local draft persistence using SharedPreferences.
- Resume preview.
- Optional AI professional-summary improvement through the existing FastAPI mobile endpoint.
- API base URL configurable with a Dart define; no AI credentials are stored in the app.

The current MVP intentionally does not claim PDF export, cloud sync, account authentication, multi-resume management or production readiness. Those require follow-on API and platform work.

## Prerequisites

- Flutter stable SDK (Dart 3.1 or newer per pubspec.yaml).
- Android Studio / Android SDK for Android builds.
- Python dependencies from the repository root for the existing FastAPI service.

## Restore the Android host project

The current repository has no tracked android/ directory. Generate the native Android host files using the installed Flutter SDK:

    cd soulskill_mobile
    flutter create --platforms=android --org ai.soulvest --project-name soulskill_mobile .

This creates the platform-specific Android project around the tracked Dart application source. Review generated Android files before committing them. The bootstrap script adds cleartext HTTP permission to the debug manifest only for emulator/LAN development. Release builds must use HTTPS.

Alternatively run:

    ./scripts/bootstrap_android.sh

from the repository root.

## Run locally

Terminal 1 — start the existing mobile API:

    python api_server.py

Terminal 2 — run Flutter (Android emulator):

    cd soulskill_mobile
    flutter pub get
    flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000

For a physical Android device, use your development computer's LAN IP, for example:

    flutter run --dart-define=API_BASE_URL=http://192.168.1.20:8000

The phone and computer must be on the same trusted network, and the API server must be reachable from the device. Do not use a LAN HTTP URL in production.

## Quality checks

    cd soulskill_mobile
    flutter pub get
    flutter analyze
    flutter test
    flutter build apk --debug

The APK build requires the Android host project to have been generated first.

## Architecture

- lib/models/ — resume data model and API serialization.
- lib/providers/ — UI state and local draft persistence.
- lib/screens/ — dashboard, editor and preview.
- lib/services/ — FastAPI client.
- lib/theme/ — SoulSkill design tokens and Material 3 theme.

The Streamlit web app and existing Python AI modules remain in place. The API server owns AI credentials; never place API keys in Flutter source or APK build configuration.
