# 🚀 Soulvest.ai Deployment Guide

## Complete Integration & Deployment Checklist

---

## 📋 Pre-Deployment Checklist

### ✅ Code Ready
- [x] All features implemented
- [x] PWA manifest.json created
- [x] Service worker implemented
- [x] SEO files (robots.txt, sitemap.xml)
- [x] Custom domain CNAME file
- [x] Environment configuration

### ✅ Requirements
- GitHub account
- Domain: soulvest.ai (purchased and configured)
- Google Gemini API key
- Streamlit Cloud account OR hosting provider

---

## 🌐 Option 1: Streamlit Cloud Deployment (RECOMMENDED)

### Step 1: Prepare GitHub Repository

1. **Push all files to GitHub:**
```powershell
cd D:\Personal\soulskill
git add .
git commit -m "Ready for soulvest.ai deployment"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Configure:
   - Repository: `your-username/soulvest-soulskill`
   - Branch: `main`
   - Main file: `app.py`
   - App URL: `soulvest` (will be soulvest.streamlit.app)

5. **Advanced Settings** → Add Secrets:
```toml
GOOGLE_API_KEY = "your_api_key_here"
```

6. Click **Deploy!**

### Step 3: Custom Domain Configuration

#### In Streamlit Cloud Dashboard:
1. Go to **Settings** → **General**
2. Find **"Custom subdomain"** section
3. Add: `soulvest`
4. Your app will be: `https://soulvest.streamlit.app`

#### Configure Your Domain (soulvest.ai):
1. Log into your domain registrar (GoDaddy, Namecheap, etc.)
2. Go to DNS Management
3. Add CNAME record:
   ```
   Type: CNAME
   Host: www
   Points to: soulvest.streamlit.app
   TTL: 1 hour
   ```
4. Add A record for root domain:
   ```
   Type: A
   Host: @
   Points to: Get IP from Streamlit Cloud settings
   TTL: 1 hour
   ```

5. In Streamlit Cloud:
   - Settings → Custom domain
   - Enter: `soulvest.ai` and `www.soulvest.ai`
   - Follow SSL certificate setup

**DNS Propagation:** Takes 1-48 hours (usually 2-6 hours)

---

## 🐳 Option 2: Self-Hosted Deployment (Advanced)

### A. Using Docker

1. **Create Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and Run:**
```powershell
docker build -t soulvest-ai .
docker run -p 8501:8501 -e GOOGLE_API_KEY="your_key" soulvest-ai
```

### B. Using VPS (DigitalOcean, AWS, etc.)

1. **Set up server (Ubuntu 22.04):**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10
sudo apt install python3.10 python3-pip -y

# Clone repository
git clone https://github.com/your-username/soulvest-soulskill.git
cd soulvest-soulskill

# Install dependencies
pip3 install -r requirements.txt

# Set environment variable
export GOOGLE_API_KEY="your_key_here"

# Run with systemd (create service file)
sudo nano /etc/systemd/system/soulvest.service
```

2. **Create systemd service:**
```ini
[Unit]
Description=Soulvest AI Resume Builder
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/soulvest-soulskill
Environment="GOOGLE_API_KEY=your_key_here"
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

3. **Enable and start:**
```bash
sudo systemctl enable soulvest
sudo systemctl start soulvest
```

### C. Configure Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name soulvest.ai www.soulvest.ai;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. **Enable SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d soulvest.ai -d www.soulvest.ai
```

---

## 📱 PWA Installation Instructions (For Users)

Once deployed, users can install Soulvest as an app:

### On Desktop (Chrome, Edge):
1. Visit soulvest.ai
2. Look for **"Install"** button in address bar
3. Click to install
4. App appears in Start Menu/Applications

### On Mobile (Android):
1. Visit soulvest.ai in Chrome
2. Tap menu (⋮) → **"Add to Home Screen"**
3. App icon appears on home screen
4. Opens like native app

### On iPhone/iPad:
1. Visit soulvest.ai in Safari
2. Tap Share button → **"Add to Home Screen"**
3. App icon appears on home screen

---

## 🔒 Security Configuration

### Environment Variables (Never commit!)

Create `.streamlit/secrets.toml` (local only):
```toml
GOOGLE_API_KEY = "your_actual_api_key"
```

**For Production:**
- Streamlit Cloud: Use Secrets Management in dashboard
- Docker: Use environment variables or Docker secrets
- VPS: Use systemd environment or .env file with restricted permissions

### Firewall Rules (VPS):
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 📊 Post-Deployment Monitoring

### 1. Add Analytics

#### Google Analytics 4
Add to `app.py` (in HTML head):
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

#### Hotjar (User Experience)
```html
<!-- Hotjar Tracking Code -->
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:YOUR_ID,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
```

### 2. Performance Monitoring

#### Streamlit Cloud:
- Built-in metrics in dashboard
- View app logs
- Monitor uptime

#### Self-Hosted:
```bash
# Monitor resource usage
htop

# Check logs
journalctl -u soulvest -f

# Monitor Nginx
tail -f /var/log/nginx/access.log
```

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

#### Streamlit Cloud:
✅ Automatic! Every push to `main` branch triggers redeployment

#### Self-Hosted with GitHub Actions:

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to VPS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /path/to/soulvest-soulskill
            git pull
            pip3 install -r requirements.txt
            sudo systemctl restart soulvest
```

---

## 🧪 Testing Checklist

Before going live:

### Functionality Tests
- [ ] All pages load correctly
- [ ] AI features work (with valid API key)
- [ ] Resume generation works
- [ ] PDF export functions
- [ ] All templates render properly
- [ ] Mobile responsive design works
- [ ] PWA install prompt appears
- [ ] Offline functionality (cached pages)

### Performance Tests
- [ ] Page load time < 3 seconds
- [ ] No console errors
- [ ] Images optimized
- [ ] No broken links

### SEO Tests
- [ ] Meta tags present
- [ ] robots.txt accessible
- [ ] sitemap.xml accessible
- [ ] HTTPS enabled
- [ ] Mobile-friendly (Google test)

### Browser Compatibility
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile browsers

---

## 🚨 Troubleshooting

### Issue: App won't start
**Solution:**
```bash
# Check logs
streamlit run app.py --logger.level=debug

# Verify dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: AI features not working
**Solution:**
- Verify API key is set correctly
- Check API key has proper permissions
- Ensure not hitting rate limits

### Issue: Custom domain not working
**Solution:**
- Verify DNS records propagated (use `nslookup soulvest.ai`)
- Check CNAME points to correct Streamlit URL
- Wait 24-48 hours for full propagation

### Issue: PWA install prompt not showing
**Solution:**
- Ensure HTTPS enabled
- Verify manifest.json is accessible
- Check browser console for errors
- Service worker must be registered

---

## 📈 Growth & Scaling

### When to Scale:
- 1,000+ daily active users
- Response time > 5 seconds
- High server CPU usage (>80%)

### Scaling Options:
1. **Streamlit Cloud Pro** ($250/month)
   - More resources
   - Custom authentication
   - Priority support

2. **Kubernetes Cluster**
   - Auto-scaling
   - Load balancing
   - High availability

3. **CDN Integration**
   - CloudFlare (free tier)
   - Faster global access
   - DDoS protection

---

## 🎯 Launch Checklist

### Pre-Launch:
- [ ] Domain purchased and configured
- [ ] SSL certificate enabled
- [ ] API keys configured in secrets
- [ ] All features tested
- [ ] Analytics setup
- [ ] Error tracking (Sentry)
- [ ] Backup strategy in place

### Launch Day:
- [ ] Deploy to production
- [ ] Verify all features work
- [ ] Submit sitemap to Google Search Console
- [ ] Submit to Bing Webmaster Tools
- [ ] Monitor logs for errors
- [ ] Test from different devices/locations

### Post-Launch:
- [ ] Monitor analytics daily (first week)
- [ ] Collect user feedback
- [ ] Fix critical bugs immediately
- [ ] Plan feature updates
- [ ] Regular backups

---

## 📞 Support Resources

### Documentation:
- Streamlit Docs: https://docs.streamlit.io
- PWA Guide: https://web.dev/progressive-web-apps/
- Google Gemini API: https://ai.google.dev/docs

### Community:
- Streamlit Forum: https://discuss.streamlit.io
- GitHub Issues: https://github.com/your-repo/issues

### Contact:
- Email: support@soulvest.ai
- GitHub: @your-username

---

## 🎉 You're Ready to Launch!

Your Soulvest AI Resume Builder is now ready for:
- ✅ Web deployment at soulvest.ai
- ✅ PWA installation on all devices
- ✅ Enterprise-grade features
- ✅ Global scalability

**Next Steps:**
1. Choose deployment option (Streamlit Cloud recommended)
2. Configure custom domain
3. Test thoroughly
4. Launch and monitor
5. Iterate based on user feedback

Good luck! 🚀

---

*Last Updated: January 30, 2026*
*Soulvest.ai - Empowering careers worldwide through AI*
