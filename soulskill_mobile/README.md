# SoulSkill Android App

A beautiful, AI-powered resume builder for Android built with Flutter.

## ✨ Features

- 📝 **Smart Resume Builder** - Create professional resumes with AI assistance
- 🎯 **Job Matching** - Match your resume with job descriptions
- 🤖 **AI Powered** - Get AI suggestions for improvements
- 📊 **ATS Optimization** - Optimize for Applicant Tracking Systems
- 💾 **Local Storage** - Save resumes locally on your device
- 🎨 **Beautiful UI** - Modern, responsive design

## 🚀 Quick Start

### Prerequisites
- Flutter 3.10+
- Android SDK API 21+

### Setup

```bash
# Get dependencies
flutter pub get

# Run app
flutter run
```

### API Connection

Ensure the backend API is running:

```bash
python api_server.py
```

The app connects to `http://10.0.2.2:8000` (emulator) or your device IP.

## 📱 Build APK

### Debug
```bash
flutter build apk --debug
```

### Release
```bash
flutter build apk --release
```

## 📂 Project Structure

```
lib/
├── main.dart                # App entry point
├── theme.dart              # Theme configuration
├── screens/                # UI screens
├── services/               # API integration
└── providers/              # State management
```

## 🔧 Tech Stack

- **Framework**: Flutter 3.10+
- **State Management**: Provider
- **Local Storage**: SharedPreferences
- **API**: HTTP + FastAPI backend
- **UI**: Material 3

## 📖 Complete Setup Guide

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:
- Detailed installation steps
- Backend setup
- Building for production
- Troubleshooting

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please follow our guidelines.

---

**Made with ❤️ by the SoulSkill Team**
