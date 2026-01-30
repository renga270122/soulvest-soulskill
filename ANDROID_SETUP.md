# ANDROID_SETUP.md - Guide to Create Android App

## Method 1: Using Streamlit Cloud + WebView (Easiest)

### Step 1: Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/resumeindia-ai.git
   git push -u origin main
   ```

2. **Deploy on Streamlit**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Branch: `main`
   - Main file: `app.py`
   - Click "Deploy"

3. **Add Secrets**
   - In Streamlit dashboard, go to App Settings
   - Secrets section, add:
   ```toml
   GOOGLE_API_KEY = "your_gemini_api_key"
   ```

4. **Get Your App URL**
   - Your app will be at: `https://yourusername-resumeindia-ai.streamlit.app`

### Step 2: Create Android WebView App

#### Option A: Using AppsGeyser (No Coding)

1. Go to [AppsGeyser.com](https://appsgeyser.com)
2. Click "Create App"
3. Select "Website"
4. Enter your Streamlit app URL
5. Customize:
   - App Name: "ResumeIndia AI"
   - Icon: Upload custom icon
   - Description: Add app description
6. Click "Create App"
7. Download APK

#### Option B: Using Android Studio (More Control)

1. **Install Android Studio**
   - Download from [developer.android.com](https://developer.android.com/studio)

2. **Create New Project**
   - Open Android Studio
   - New Project → Empty Activity
   - Name: "ResumeIndiaAI"
   - Package: "com.resumeindia.ai"
   - Language: Java/Kotlin
   - Minimum SDK: API 21

3. **Add WebView**
   
   **activity_main.xml:**
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
       android:layout_width="match_parent"
       android:layout_height="match_parent">
       
       <WebView
           android:id="@+id/webview"
           android:layout_width="match_parent"
           android:layout_height="match_parent" />
   </RelativeLayout>
   ```
   
   **MainActivity.java:**
   ```java
   package com.resumeindia.ai;
   
   import android.os.Bundle;
   import android.webkit.WebSettings;
   import android.webkit.WebView;
   import android.webkit.WebViewClient;
   import androidx.appcompat.app.AppCompatActivity;
   
   public class MainActivity extends AppCompatActivity {
       private WebView webView;
       
       @Override
       protected void onCreate(Bundle savedInstanceState) {
           super.onCreate(savedInstanceState);
           setContentView(R.layout.activity_main);
           
           webView = findViewById(R.id.webview);
           WebSettings webSettings = webView.getSettings();
           webSettings.setJavaScriptEnabled(true);
           webSettings.setDomStorageEnabled(true);
           
           webView.setWebViewClient(new WebViewClient());
           webView.loadUrl("https://yourusername-resumeindia-ai.streamlit.app");
       }
       
       @Override
       public void onBackPressed() {
           if (webView.canGoBack()) {
               webView.goBack();
           } else {
               super.onBackPressed();
           }
       }
   }
   ```

4. **Add Permissions**
   
   **AndroidManifest.xml:**
   ```xml
   <uses-permission android:name="android.permission.INTERNET" />
   <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
   ```

5. **Build APK**
   - Build → Build Bundle(s) / APK(s) → Build APK(s)
   - Find APK in `app/build/outputs/apk/debug/`

---

## Method 2: Using Kivy/BeeWare (Native Python)

### Using Buildozer (For Linux/Mac)

1. **Install Buildozer**
   ```bash
   pip install buildozer
   ```

2. **Initialize**
   ```bash
   buildozer init
   ```

3. **Edit buildozer.spec**
   ```ini
   [app]
   title = ResumeIndia AI
   package.name = resumeindia
   package.domain = ai.resumeindia
   source.dir = .
   source.include_exts = py,png,jpg,kv,atlas,ttf
   requirements = python3,kivy,streamlit
   ```

4. **Build**
   ```bash
   buildozer -v android debug
   ```

### Using BeeWare

1. **Install BeeWare**
   ```bash
   pip install briefcase
   ```

2. **Create Project**
   ```bash
   briefcase new
   ```

3. **Build Android**
   ```bash
   briefcase create android
   briefcase build android
   briefcase run android
   ```

---

## Method 3: Progressive Web App (PWA)

Make your app installable as PWA:

1. **Create manifest.json**
   ```json
   {
     "name": "ResumeIndia AI",
     "short_name": "ResumeAI",
     "description": "AI-Powered ATS-Friendly Resume Builder",
     "start_url": "/",
     "display": "standalone",
     "background_color": "#667eea",
     "theme_color": "#667eea",
     "icons": [
       {
         "src": "/icon-192.png",
         "sizes": "192x192",
         "type": "image/png"
       },
       {
         "src": "/icon-512.png",
         "sizes": "512x512",
         "type": "image/png"
       }
     ]
   }
   ```

2. Users can "Add to Home Screen" on mobile browsers

---

## Recommended Approach

**For Quick Deployment:**
→ Streamlit Cloud + AppsGeyser (No coding, 30 minutes)

**For Better Control:**
→ Streamlit Cloud + Android Studio WebView (2-3 hours)

**For Native Experience:**
→ BeeWare/Kivy (Advanced, 1-2 days)

---

## Testing Your Android App

1. **Enable Developer Options** on Android device
2. **Enable USB Debugging**
3. Connect device via USB
4. Install APK:
   ```bash
   adb install app-debug.apk
   ```

Or simply share APK file and install directly on device.

---

## Publishing to Google Play Store

1. **Create Developer Account** ($25 one-time fee)
2. **Generate Signed APK** in Android Studio
3. **Create Store Listing**:
   - App name: ResumeIndia AI
   - Description: AI-Powered Resume Builder
   - Screenshots: 2-8 images
   - Category: Business/Productivity
4. **Submit for Review**
5. **Wait for Approval** (1-3 days)

---

## Troubleshooting

### WebView shows blank page
- Check internet connection
- Verify Streamlit app URL is correct
- Enable JavaScript in WebView settings

### App crashes on startup
- Add internet permissions in manifest
- Check Android API level compatibility
- Verify Streamlit app is running

### PDF download not working
- WebView may block downloads
- Implement DownloadListener in Android
- Or use "Share" feature instead

---

**Need Help?**
- GitHub Issues
- Email: support@resumeindia.ai
