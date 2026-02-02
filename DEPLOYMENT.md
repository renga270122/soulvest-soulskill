# SoulSkill AI - Resume Builder Deployment Guide

## 🚀 Quick Deploy to Streamlit Cloud (FREE)

### Step 1: Prepare Your Repository

Your code is already on GitHub at: `https://github.com/renga270122/soulvest-soulskill.git`

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in:
   - **Repository**: `renga270122/soulvest-soulskill`
   - **Branch**: `main`
   - **Main file path**: `app_enhanced.py`
   - **App URL**: Choose `soulskill` (will be `soulskill.streamlit.app`)

5. Click "Advanced settings" and add your secrets:
   ```toml
   [secrets]
   GOOGLE_API_KEY = "your-google-api-key-here"
   ```

6. Click "Deploy!"

### Step 3: Domain Setup

#### Option A: Use Free Streamlit Subdomain
- Your app will be at: `https://soulskill.streamlit.app`
- Free, instant, no configuration needed

#### Option B: Custom Domain (soulskill.ai)

**Purchase Domain:**
- Go to [Namecheap](https://namecheap.com) or [Cloudflare](https://cloudflare.com)
- Search for `soulskill.ai` (~$12/year)
- Complete purchase

**Configure Custom Domain:**
1. In Streamlit Cloud dashboard, go to your app settings
2. Click "Custom domain"
3. Enter: `soulskill.ai`
4. Follow the DNS setup instructions provided
5. Add CNAME record in your domain registrar:
   ```
   CNAME  @  soulskill.streamlit.app
   ```

#### Option C: Subdomain on soulvest.ai

**If you already own soulvest.ai:**
1. In your DNS settings, add:
   ```
   CNAME  resume  soulskill.streamlit.app
   ```
2. Access your app at: `https://resume.soulvest.ai`

### Step 4: Alternative - Deploy to Vercel (For Custom Domain)

If you want more control:

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   cd D:/Personal/soulskill
   vercel
   ```

4. Follow prompts and connect your custom domain

### Step 5: Environment Variables

Make sure to set these in your deployment platform:
- `GOOGLE_API_KEY` - Your Google Gemini API key

### 🎯 Recommended Approach

**For Fastest Launch:**
1. Deploy to Streamlit Cloud (5 minutes) → `soulskill.streamlit.app`
2. Test everything works
3. Buy `soulskill.ai` domain
4. Point domain to Streamlit app
5. Also set up `resume.soulvest.ai` subdomain

**Free Tier Limits:**
- Streamlit Cloud: 1 app free (unlimited viewers)
- Upgrade for multiple apps or custom resources

### 📊 Post-Deployment Checklist

- [ ] App loads successfully
- [ ] All templates display correctly
- [ ] AI features work (check API key)
- [ ] Download buttons functional (PDF, DOCX, etc.)
- [ ] Mobile responsive design working
- [ ] Custom domain configured (if applicable)
- [ ] Analytics/tracking added (optional)
- [ ] SEO meta tags added

### 🔧 Troubleshooting

**If PDF download fails:**
- Add to `packages.txt`: `wkhtmltopdf`

**If imports fail:**
- Check all packages are in `requirements.txt`

**If secrets not loading:**
- Verify secrets are in Streamlit Cloud settings
- Format must be exact TOML syntax

### 📈 Next Steps After Deployment

1. **Test thoroughly** on mobile and desktop
2. **Share** with friends for feedback
3. **Monitor** usage in Streamlit Cloud dashboard
4. **Iterate** based on user feedback
5. **Market** on LinkedIn, Twitter, ProductHunt

---

Need help? The deployment is straightforward - should take under 10 minutes! 🚀
