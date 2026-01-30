# 🚀 QUICK START GUIDE

## Get Started in 5 Minutes!

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Set Up AI (Optional but Recommended)
1. Get free Google Gemini API key: https://makersuite.google.com/app/apikey
2. Set environment variable:
```powershell
$env:GOOGLE_API_KEY="your_key_here"
```

### Step 3: Run the App
```powershell
streamlit run app.py
```

### Step 4: Open in Browser
- Automatically opens at: http://localhost:8501
- Or manually open the URL shown in terminal

---

## 🎯 Creating Your First Resume

1. **Choose Profile Type**: Fresher or Experienced
2. **Enter Personal Details**: Name, email, phone, location
3. **Select a Template**: Pick from 10+ options
4. **AI Generate Summary**: Click "Generate with AI" (if enabled)
5. **Add Skills**: Technical + Soft skills
6. **Add Experience**: Work history or internships
7. **Add Projects**: Showcase your work
8. **Add Education**: Degrees and certifications
9. **Preview**: See your resume in real-time
10. **Download**: Get PDF or HTML

---

## 🤖 Enabling AI Features

### Option 1: Environment Variable (Temporary)
```powershell
# Windows PowerShell
$env:GOOGLE_API_KEY="your_key"

# Then run
streamlit run app.py
```

### Option 2: Create .env File (Permanent)
```powershell
# Copy example file
Copy-Item .env.example .env

# Edit .env and add your key
notepad .env
```

Add this line:
```
GOOGLE_API_KEY=your_actual_key_here
```

Then run normally:
```powershell
streamlit run app.py
```

---

## 📊 Using ATS Checker

1. Complete your resume (all steps)
2. Go to "ATS Check" step
3. Paste job description you're applying for
4. Click "Analyze ATS Compatibility"
5. See your score (aim for 75+!)
6. Add missing keywords
7. Re-check until score improves

---

## 💡 Pro Tips

### Getting 80+ ATS Score:
1. Use keywords from job description
2. Keep format simple (no tables)
3. Use standard section names
4. Add numbers (increased by 30%)
5. Use action verbs (Led, Developed, Managed)

### For Freshers:
- Focus on projects and coursework
- Highlight relevant certifications
- Emphasize soft skills
- Mention internships/training

### For Experienced:
- Lead with achievements
- Quantify results
- Show career progression
- Include leadership roles

---

## 🐛 Troubleshooting

### AI Not Working?
- Check if GOOGLE_API_KEY is set
- Verify API key is valid
- Check internet connection
- Offline mode still works (no AI features)

### PDF Not Generating?
- Install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
- Alternative: Download HTML version

### App Won't Start?
```powershell
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Clear cache
streamlit cache clear

# Run again
streamlit run app.py
```

---

## 📱 Mobile Access

### On Same WiFi:
```powershell
streamlit run app.py --server.address=0.0.0.0
```
Then access from phone: `http://YOUR_PC_IP:8501`

### Deploy Online (Free):
1. Push to GitHub
2. Deploy on Streamlit Cloud: https://share.streamlit.io
3. Access from anywhere!

---

## 🎓 Video Tutorials (Coming Soon)
- [ ] Complete walkthrough
- [ ] AI features demo
- [ ] ATS optimization tips
- [ ] Android app creation

---

## 📞 Need Help?
- GitHub Issues: Report bugs
- Email: support@resumeindia.ai
- Documentation: README.md

---

**Made with ❤️ for Indian Job Seekers**
