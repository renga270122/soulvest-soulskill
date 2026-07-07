# Quick Start Guide - SoulSkill Android App

## 🚀 Super Simple Setup (3 Steps)

### Step 1: Install Flutter (One Time Only)

**Option A - Automatic:**
```powershell
winget install --id=Google.Flutter -e
```

**Option B - Manual:**
1. Download from: https://flutter.dev/docs/get-started/install/windows
2. Extract to `C:\src\flutter`
3. Add to PATH: `C:\src\flutter\bin`
4. Restart PowerShell

Verify:
```powershell
flutter doctor
```

---

### Step 2: Run Setup Script

```powershell
cd D:\Personal\soulskill
.\setup_android_app.ps1
```

This installs everything automatically! ✅

---

### Step 3: Start the App

**Terminal 1 (Backend):**
```powershell
.\start_backend.ps1
```

**Terminal 2 (Mobile App):**
```powershell
.\start_app.ps1
```

Done! 🎉

---

## 📱 Before Running

Make sure you have **one** of these:
- ✅ Android Studio with emulator running
- ✅ Android phone connected via USB (Developer mode ON)
- ✅ Visual Studio with Android emulator

Check devices:
```powershell
flutter devices
```

---

## 🆘 Troubleshooting

**"Flutter not found"**
- Install Flutter (Step 1)
- Restart PowerShell

**"No devices found"**
- Start Android Studio emulator
- Or connect phone with USB debugging

**"API connection failed"**
- Make sure backend is running (`.\start_backend.ps1`)
- Check: http://localhost:8000/health

---

## 🎯 What You Get

- 📱 Beautiful Android app
- 🤖 AI-powered resume builder
- 🎯 Job matching
- 📊 ATS optimization
- 💾 Local storage

**Need help?** Just ask!
