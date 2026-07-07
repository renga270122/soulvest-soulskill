# SoulSkill Deployment Guide - Android & Backend

## 🚀 Deployment Overview

This guide covers deploying both the Flutter Android app and the FastAPI backend.

## 📱 Android App Deployment

### Option 1: Direct APK Installation (Testing)

1. **Build Debug APK**
   ```bash
   cd soulskill_mobile
   flutter build apk --debug
   ```

2. **Install on Device/Emulator**
   ```bash
   adb install build/app/outputs/flutter-apk/app-debug.apk
   ```

### Option 2: Release APK (User Distribution)

1. **Create Signing Key**
   ```bash
   keytool -genkey -v -keystore release.jks \
     -keyalg RSA -keysize 2048 \
     -validity 10000 -alias soulskill
   ```

2. **Create key.properties File**
   ```bash
   # android/key.properties
   storePassword=your_password
   keyPassword=your_password
   keyAlias=soulskill
   storeFile=../release.jks
   ```

3. **Build Release APK**
   ```bash
   flutter build apk --release
   ```
   Output: `build/app/outputs/flutter-apk/app-release.apk`

### Option 3: Google Play Store (Production)

1. **Build App Bundle**
   ```bash
   flutter build appbundle --release
   ```

2. **Upload to Play Store**
   - Visit [Google Play Console](https://play.google.com/console)
   - Create new app
   - Upload `app-release.aab`
   - Complete store listing
   - Submit for review

## 🔧 Backend Deployment

### Option 1: Local/Development Server

```bash
# Install dependencies
pip install -r api_requirements.txt

# Run server
python api_server.py

# Server runs on http://localhost:8000
```

### Option 2: Heroku Deployment

1. **Create Procfile**
   ```
   web: uvicorn api_server:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy**
   ```bash
   heroku login
   heroku create soulskill-api
   git push heroku main
   ```

3. **Set API URL in App**
   - Update `lib/services/api_client.dart`
   - Change baseUrl to: `https://soulskill-api.herokuapp.com`

### Option 3: AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Image: Ubuntu 22.04
   - Instance Type: t2.micro (free tier)
   - Security Group: Allow port 8000

2. **Connect via SSH**
   ```bash
   ssh -i key.pem ubuntu@your-ec2-ip
   ```

3. **Setup Server**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3 python3-pip python3-venv -y
   
   # Clone repo
   git clone <your-repo>
   cd soulskill
   
   # Create virtual env
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r api_requirements.txt
   ```

4. **Run with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 api_server:app
   ```

5. **Setup with Systemd**
   ```bash
   # /etc/systemd/system/soulskill.service
   [Unit]
   Description=SoulSkill API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/soulskill
   ExecStart=/home/ubuntu/soulskill/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 api_server:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   sudo systemctl enable soulskill
   sudo systemctl start soulskill
   ```

### Option 4: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build & Run**
   ```bash
   docker build -t soulskill-api .
   docker run -p 8000:8000 soulskill-api
   ```

3. **Deploy to Docker Hub**
   ```bash
   docker tag soulskill-api your-username/soulskill-api
   docker push your-username/soulskill-api
   ```

## 🔗 Connect App to Backend

### For Development (Emulator)
- Already configured: `http://10.0.2.2:8000`

### For Production (Device)
Edit `lib/services/api_client.dart`:
```dart
static const String baseUrl = 'https://your-api-domain.com';
```

## ✅ Testing Deployment

```bash
# Test API health
curl http://your-server:8000/health

# Test from app
flutter run -d your-device
```

## 📊 Monitoring

### Local Development
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Production
- Monitor logs: `sudo journalctl -u soulskill -f`
- Check status: `sudo systemctl status soulskill`

## 🔒 Security Best Practices

1. **Use HTTPS** - Get SSL certificate (Let's Encrypt)
2. **Environment Variables** - Store secrets in `.env`
3. **CORS** - Restrict to your app domain
4. **Rate Limiting** - Prevent API abuse
5. **Authentication** - Add API key validation

## 📈 Scaling

For high traffic:
1. Use load balancer (nginx)
2. Run multiple API instances
3. Use database (PostgreSQL)
4. Add caching (Redis)
5. Use CDN for assets

## 🆘 Troubleshooting

**App can't connect to API**
- Verify API is running
- Check firewall settings
- Confirm correct IP/domain in app
- Check CORS settings

**Slow API responses**
- Scale to more instances
- Add caching
- Optimize database queries
- Use CDN

**Memory issues on EC2**
- Use t2.small or larger
- Implement rate limiting
- Monitor with CloudWatch

---

**For detailed API documentation, visit `/docs` after running the server.**
