import streamlit as st
from streamlit_lottie import st_lottie
import requests
import re
import json
import os
import pdfkit
import tempfile
import base64
import shutil
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Config files
from stream_config import STREAM_OPTIONS
from education_config import DEGREE_OPTIONS, SCHOOL_PROGRAMS
from template_config import TEMPLATES, INDIAN_TEMPLATES
from industry_config import INDUSTRY_OPTIONS, INDUSTRY_KEYWORDS

st.set_page_config(
    page_title="ResumeIndia - Professional Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-responsive and attractive design
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    h1 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
    }
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        h1 {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def sanitize_text(text):
    if not text:
        return ""
    return text.encode("utf-8", errors="ignore").decode("utf-8").replace("â", "-").replace("ðŸ", "").replace("ï", "").replace("ÕŸ", "").replace("ðÝŽ“", "")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "work_entries" not in st.session_state:
    st.session_state.work_entries = []
if "education_entries" not in st.session_state:
    st.session_state.education_entries = []
if "certification_entries" not in st.session_state:
    st.session_state.certification_entries = []
if "project_entries" not in st.session_state:
    st.session_state.project_entries = []
if "language_entries" not in st.session_state:
    st.session_state.language_entries = []
if "profile_type" not in st.session_state:
    st.session_state.profile_type = None

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("📄 ResumeIndia")
    st.markdown("---")
    
    if st.session_state.step > 0:
        progress = (st.session_state.step / 12) * 100
        st.progress(progress / 100)
        st.caption(f"Progress: {int(progress)}%")
        
        st.markdown("### 📍 Navigation")
        steps = ["Profile Type", "Personal Info", "Template", "Summary", "Skills", 
                "Experience", "Work History", "Projects", "Education", "Certifications", 
                "Social Links", "Preview & Download", "Extra Features"]
        for i, step_name in enumerate(steps):
            if i < st.session_state.step:
                st.markdown(f"✅ {step_name}")
            elif i == st.session_state.step:
                st.markdown(f"▶️ **{step_name}**")
            else:
                st.markdown(f"⚪ {step_name}")
    
    st.markdown("---")
    st.caption("🇮🇳 Made for Indian Professionals")
    st.caption("💼 Freshers & Experienced")

# Main Content
if st.session_state.step == 0:
    # Welcome Screen
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
    
    st.markdown("<h1 style='text-align: center;'>📄 ResumeIndia</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #666;'>Professional Resume Builder for Indian Freshers & Professionals</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>🎯 Industry-Specific</h3>
            <p>Templates for IT, Healthcare, Finance, Education, Manufacturing & more</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>📱 Mobile-Friendly</h3>
            <p>Create resumes on any device - Desktop, Tablet, or Phone</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3>🇮🇳 India-Ready</h3>
            <p>Formats for Indian companies with location, languages, and more</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 Start Building Your Resume", use_container_width=True):
            next_step()

elif st.session_state.step == 1:
    # Profile Type Selection
    st.title("👤 Choose Your Profile Type")
    st.markdown("Tell us about your career stage so we can customize your resume")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎓 Fresher\n\nNo work experience\nRecent graduate or student", use_container_width=True, key="fresher_btn"):
            st.session_state.profile_type = "fresher"
            next_step()
    
    with col2:
        if st.button("💼 Experienced\n\nHave work experience\nCareer professional", use_container_width=True, key="exp_btn"):
            st.session_state.profile_type = "experienced"
            next_step()

elif st.session_state.step == 2:
    # Personal Information
    st.title("📝 Personal Information")
    st.markdown("Let's start with your basic details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.full_name = st.text_input("Full Name *", value=st.session_state.get("full_name", ""))
        st.session_state.email = st.text_input("Email Address *", value=st.session_state.get("email", ""))
        st.session_state.phone = st.text_input("Phone Number *", value=st.session_state.get("phone", ""), 
                                               placeholder="+91-XXXXX-XXXXX")
        st.session_state.city = st.text_input("City *", value=st.session_state.get("city", ""))
    
    with col2:
        st.session_state.state = st.text_input("State *", value=st.session_state.get("state", ""))
        st.session_state.pincode = st.text_input("Pincode", value=st.session_state.get("pincode", ""))
        st.session_state.industry = st.selectbox("Target Industry *", ["Select Industry"] + INDUSTRY_OPTIONS,
                                                 index=0 if "industry" not in st.session_state else 
                                                 INDUSTRY_OPTIONS.index(st.session_state.industry) + 1)
        st.session_state.job_title_target = st.text_input("Target Job Title *", 
                                                          value=st.session_state.get("job_title_target", ""),
                                                          placeholder="e.g., Software Developer, Marketing Manager")
    
    st.markdown("---")
    st.markdown("#### Languages Known")
    col1, col2, col3 = st.columns(3)
    with col1:
        lang_name = st.text_input("Language", key="lang_input")
    with col2:
        lang_prof = st.selectbox("Proficiency", ["Native", "Fluent", "Professional", "Basic"], key="prof_input")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Language"):
            if lang_name:
                st.session_state.language_entries.append({"language": lang_name, "proficiency": lang_prof})
                st.success(f"Added {lang_name}!")
    
    if st.session_state.language_entries:
        st.markdown("**Languages Added:**")
        for idx, lang in enumerate(st.session_state.language_entries):
            st.write(f"• {lang['language']} - {lang['proficiency']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            if all([st.session_state.get("full_name"), st.session_state.get("email"), 
                   st.session_state.get("phone"), st.session_state.get("city"), 
                   st.session_state.get("state")]):
                next_step()
            else:
                st.error("Please fill all required fields (marked with *)")

elif st.session_state.step == 3:
    st.title("🎨 Choose Your Resume Template")
    st.markdown("Select a template that matches your industry and style")
    
    # Combine templates
    all_templates = {**TEMPLATES, **INDIAN_TEMPLATES}
    template_names = list(all_templates.keys())
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_template = st.selectbox("Select Template", template_names)
        st.session_state.template = selected_template
        
        layout_choice = st.radio("Layout Style", ["Single Column", "Two Column"])
        st.session_state.layout = layout_choice
        
        font = all_templates[selected_template]['font']
        color = all_templates[selected_template]['color']
        
        st.markdown(f"**Font:** {font}")
        st.markdown(f"**Primary Color:**")
        st.markdown(f"<div style='width:100px;height:40px;background-color:{color};border-radius:8px;border:2px solid #ddd;'></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📱 Template Preview")
        sample_name = st.session_state.get("full_name", "Your Name")
        sample_title = st.session_state.get("job_title_target", "Professional Title")
        
        preview_html = f"""
        <div style="border:2px solid #ddd;border-radius:12px;padding:20px;background:white;">
            <div style="font-family:{font};color:{color};">
                <h2 style="margin:0;color:{color};">{sample_name}</h2>
                <p style="font-size:1.1rem;margin:5px 0;"><strong>{sample_title}</strong></p>
                <p style="color:#666;">📧 email@example.com | 📱 +91-XXXXX-XXXXX | 📍 Mumbai, Maharashtra</p>
                <hr style="border:1px solid {color};margin:15px 0;">
                <h3 style="color:{color};">Professional Summary</h3>
                <p>Experienced professional with expertise in...</p>
                <h3 style="color:{color};">Key Skills</h3>
                <p>• Skill 1 • Skill 2 • Skill 3</p>
            </div>
        </div>
        """
        st.markdown(preview_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            next_step()

elif st.session_state.step == 4:
    st.header("🌟 Soulful Summary")
    summary_input = st.text_area("Write your summary", value=st.session_state.get("summary", ""))
    if st.button("💾 Save Summary"):
        st.session_state.summary = sanitize_text(summary_input)
        st.success("Saved!")
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

elif st.session_state.step == 3:
    st.header("🧠 Skills")
    skills_input = st.text_area("List your skills", value=st.session_state.get("skills", ""))
    if st.button("💾 Save Skills"):
        st.session_state.skills = sanitize_text(skills_input)
        st.success("Saved!")
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

elif st.session_state.step == 4:
    st.header("💼 Experience Highlights")
    exp_input = st.text_area("Describe your experience", value=st.session_state.get("experience", ""))
    if st.button("💾 Save Experience"):
        st.session_state.experience = sanitize_text(exp_input)
        st.success("Saved!")
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)
elif st.session_state.step == 5:
    st.header("📜 Work History")
    job_title = st.text_input("Job Title", value=st.session_state.get("job_title", ""))
    company_name = st.text_input("Company Name", value=st.session_state.get("company_name", ""))
    duration = st.text_input("Duration", value=st.session_state.get("duration", ""))
    responsibilities = st.text_area("Responsibilities", value=st.session_state.get("responsibilities", ""))

    if st.button("💾 Save Work Entry"):
        st.session_state.job_title = job_title
        st.session_state.company_name = company_name
        st.session_state.duration = duration
        st.session_state.responsibilities = responsibilities
        st.success("Saved!")

    if st.button("➕ Add Entry"):
        st.session_state.work_entries.append({
            "title": sanitize_text(job_title),
            "company": sanitize_text(company_name),
            "duration": sanitize_text(duration),
            "responsibilities": sanitize_text(responsibilities)
        })
        st.success("Entry added!")

    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

elif st.session_state.step == 6:
    st.header("🧪 Project Highlights")
    proj_input = st.text_area("Describe key projects", value=st.session_state.get("projects", ""))
    if st.button("💾 Save Projects"):
        st.session_state.projects = sanitize_text(proj_input)
        st.success("Saved!")
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

elif st.session_state.step == 7:
    st.header("🎓 Education")
    st.session_state.degree = st.selectbox("Degree", DEGREE_OPTIONS)
    st.session_state.stream = st.selectbox("Stream", STREAM_OPTIONS)
    st.session_state.university = st.text_input("University")
    st.session_state.institution = st.text_input("Institution")
    st.session_state.grad_year = st.text_input("Graduation Year")
    st.session_state.grade = st.text_input("Grade")
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

elif st.session_state.step == 8:
    st.header("🔗 Social Links")
    st.session_state.github = st.text_input("GitHub URL")
    st.session_state.linkedin = st.text_input("LinkedIn URL")
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)
elif st.session_state.step == 9:
    st.header("📄 Resume Preview")

    template = st.session_state.template
    font = TEMPLATES[template]["font"]
    color = TEMPLATES[template]["color"]
    layout = st.session_state.layout

    # Profile Photo Upload
    st.markdown("### 🖼️ Upload Your Profile Photo (Optional)")
    photo = st.file_uploader("Upload a professional photo", type=["jpg", "jpeg", "png"])
    photo_html = ""
    if photo:
        encoded = base64.b64encode(photo.read()).decode()
        photo_html = f"<img src='data:image/png;base64,{encoded}' style='width:100px;border-radius:8px;margin-bottom:10px;'/>"

    # Work History HTML
    work_html = ""
    for entry in st.session_state.work_entries:
        work_html += f"<p><strong>{entry['title']}</strong><br>{entry['company']} ({entry['duration']})<br>{entry['responsibilities']}</p>"

    # Social Links
    social_html = ""
    if st.session_state.get("github"):
        social_html += f"<a href='{st.session_state.github}' target='_blank'>GitHub</a><br>"
    if st.session_state.get("linkedin"):
        social_html += f"<a href='{st.session_state.linkedin}' target='_blank'>LinkedIn</a>"

    # Resume HTML
    if layout == "Single Column":
        html_resume = f"""
        <html><head><style>
        body {{
            font-family: '{font}', sans-serif;
            color: {color};
            padding: 40px;
            line-height: 1.6;
        }}
        h3 {{
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }}
        </style></head><body>
        {photo_html}
        <h2>{sanitize_text('Renganathan')}</h2>
        <p><strong>Founder, Soulvest.ai</strong></p>
        <h3>🌟 Summary</h3><p>{sanitize_text(st.session_state.get("summary", ""))}</p>
        <h3>🧠 Skills</h3><p>{sanitize_text(st.session_state.get("skills", ""))}</p>
        <h3>💼 Experience Highlights</h3><p>{sanitize_text(st.session_state.get("experience", ""))}</p>
        <h3>📜 Work History</h3>{work_html}
        <h3>🧪 Project Highlights</h3><p>{sanitize_text(st.session_state.get("projects", ""))}</p>
        <h3>🎓 Higher Education</h3>
        <p>{sanitize_text(st.session_state.get("degree", ""))} in {sanitize_text(st.session_state.get("stream", ""))}<br>
        {sanitize_text(st.session_state.get("institution", ""))}, {sanitize_text(st.session_state.get("university", ""))}<br>
        Graduation Year: {sanitize_text(st.session_state.get("grad_year", ""))} | Grade: {sanitize_text(st.session_state.get("grade", ""))}</p>
        <h3>🏫 School Education</h3>
        <p>{sanitize_text(st.session_state.get("school_program", ""))}<br>
        {sanitize_text(st.session_state.get("school_name", ""))} | Year: {sanitize_text(st.session_state.get("school_year", ""))}</p>
        <h3>🔗 Social Links</h3><p>{social_html}</p>
        <h3>🌐 Portfolio</h3>
        <p><a href='https://soulvest.ai'>https://soulvest.ai</a></p>
        <img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=https://soulvest.ai'/>
        <br><br><p style='text-align:center;'>✨ Crafted with clarity. Powered by SoulSkill.</p>
        </body></html>
        """
    else:
        html_resume = f"""
        <html><head><style>
        body {{
            font-family: '{font}', sans-serif;
            color: {color};
            padding: 30px;
            line-height: 1.6;
        }}
        .container {{
            display: flex;
            gap: 30px;
        }}
        .left {{
            width: 35%;
        }}
        .right {{
            width: 65%;
        }}
        h3 {{
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }}
        </style></head><body>
        <div class="container">
        <div class="left">
            {photo_html}
            <h3>📍 Contact</h3>
            <p>📧 hello@soulskill.ai<br>🌐 https://soulvest.ai</p>
            <h3>🎓 Education</h3>
            <p>{sanitize_text(st.session_state.get("degree", ""))}<br>{sanitize_text(st.session_state.get("institution", ""))}</p>
            <h3>🛠️ Skills</h3>
            <p>{sanitize_text(st.session_state.get("skills", ""))}</p>
            <h3>🔗 Links</h3>
            <p>{social_html}</p>
        </div>
        <div class="right">
            <h2>{sanitize_text('Renganathan')}</h2>
            <p><strong>Founder, Soulvest.ai</strong></p>
            <h3>🌟 Summary</h3><p>{sanitize_text(st.session_state.get("summary", ""))}</p>
            <h3>💼 Experience</h3><p>{sanitize_text(st.session_state.get("experience", ""))}</p>
            <h3>📜 Work History</h3>{work_html}
            <h3>🧪 Projects</h3><p>{sanitize_text(st.session_state.get("projects", ""))}</p>
            <h3>🌐 Portfolio</h3>
            <p><a href='https://soulvest.ai'>https://soulvest.ai</a></p>
            <img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=https://soulvest.ai'/>
        </div>
        </div>
        <br><p style='text-align:center;'>✨ Crafted with clarity. Powered by SoulSkill.</p>
        </body></html>
        """

    st.markdown(html_resume, unsafe_allow_html=True)

    try:
        wkhtml_path = shutil.which("wkhtmltopdf") or r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdfkit.from_string(html_resume, tmp.name, configuration=config)
            st.download_button("📥 Download Resume PDF", data=open(tmp.name, "rb").read(), file_name="SoulSkill_Resume.pdf")
    except Exception as e:
        st.error(f"PDF generation failed: {e}")

    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)
elif st.session_state.step == 10:
    st.header("💌 Cover Letter Generator")

    tone = st.selectbox("Choose your tone", ["Confident", "Humble", "Visionary"])
    cover_letter = ""

    if st.button("Generate Cover Letter"):
        work_lines = "\n".join([
            f"{e['title']} at {e['company']} ({e['duration']})"
            for e in st.session_state.work_entries
        ])

        cover_letter = f"""
Dear Hiring Manager,

I am writing to express my interest in the role at your esteemed organization. With a background in {sanitize_text(st.session_state.get("experience", ""))}, and a passion for {sanitize_text(st.session_state.get("skills", ""))}, I believe I bring both skill and soul to the opportunity.

My journey has been shaped by roles such as:
{sanitize_text(work_lines)}

I am excited to contribute with {tone.lower()} energy and a commitment to growth. I would welcome the opportunity to discuss how my experience and values align with your team’s mission.

With gratitude,  
Renganathan
        """.strip()

    if cover_letter:
        st.text_area("Your Cover Letter", value=cover_letter, height=300)
        if st.button("💾 Save Cover Letter as PDF"):
            try:
                wkhtml_path = shutil.which("wkhtmltopdf") or r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
                config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    pdfkit.from_string(f"<html><body><pre>{cover_letter}</pre></body></html>", tmp.name, configuration=config)
                    st.download_button("📥 Download Cover Letter PDF", data=open(tmp.name, "rb").read(), file_name="SoulSkill_CoverLetter.pdf")
            except Exception as e:
                st.error(f"Cover letter PDF failed: {e}")

    # ATS Optimizer
    st.markdown("---")
    st.header("🧠 ATS Optimizer")

    job_desc = st.text_area("Paste Job Description")
    resume_text = " ".join([
        sanitize_text(st.session_state.get("summary", "")),
        sanitize_text(st.session_state.get("skills", "")),
        sanitize_text(st.session_state.get("experience", "")),
        sanitize_text(st.session_state.get("certifications", "")),
        sanitize_text(st.session_state.get("achievements", "")),
        sanitize_text(st.session_state.get("projects", "")),
        " ".join([f"{e['title']} {e['company']} {e['responsibilities']}" for e in st.session_state.work_entries])
    ])

    if st.button("Analyze ATS Match"):
        if job_desc and resume_text:
            try:
                vectorizer = CountVectorizer().fit_transform([job_desc, resume_text])
                score = cosine_similarity(vectorizer)[0][1]
                st.metric("ATS Match Score", f"{round(score * 100)} / 100")

                job_keywords = set(re.findall(r'\b\w+\b', job_desc.lower()))
                resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
                missing_keywords = job_keywords - resume_words

                if missing_keywords:
                    st.warning("🧠 Missing Keywords:")
                    st.write(", ".join(sorted(missing_keywords)))
                else:
                    st.success("✅ Your resume covers all major keywords!")
            except Exception as e:
                st.error(f"ATS analysis failed: {e}")
        else:
            st.error("Please paste both job description and resume.")
elif st.session_state.step == 11:
    st.header("🎯 Career Suggestions Based on Your Role")

    user_role = st.text_input("Enter your current role (e.g., Software Engineer, Marketing Manager)")

    if user_role:
        st.markdown(f"**Current Role:** {user_role}")
        st.markdown("### 🔍 Suggested Job Roles")
        role_jobs = [
            f"{user_role} II",
            f"Senior {user_role}",
            f"{user_role} Lead",
            f"{user_role} Manager",
            f"{user_role} Consultant",
            f"{user_role} Architect",
            f"{user_role} Coach",
            f"{user_role} Trainer",
            f"{user_role} Strategist",
            f"{user_role} Evangelist"
        ]
        for job in role_jobs:
            st.markdown(f"- {job}")

        st.markdown("### 📚 Recommended Certifications")
        role_certs = [
            f"{user_role} Fundamentals",
            f"Advanced {user_role} Techniques",
            f"{user_role} Leadership Program",
            f"{user_role} Bootcamp",
            f"{user_role} Certification by Coursera",
            f"{user_role} Masterclass by Udemy",
            f"{user_role} Specialization by edX",
            f"{user_role} Professional Certificate",
            f"{user_role} AI Integration",
            f"{user_role} Agile & DevOps"
        ]
        for cert in role_certs:
            st.markdown(f"- {cert}")

    # Resume Health Score
    st.markdown("---")
    st.header("📊 Resume Health Score")

    criteria = {
        "Summary": bool(st.session_state.get("summary")),
        "Skills": bool(st.session_state.get("skills")),
        "Experience": bool(st.session_state.get("experience")),
        "Work History": len(st.session_state.work_entries) > 0,
        "Projects": bool(st.session_state.get("projects")),
        "Education": bool(st.session_state.get("degree")) and bool(st.session_state.get("stream")),
        "Social Links": bool(st.session_state.get("github")) or bool(st.session_state.get("linkedin"))
    }

    score = sum(criteria.values()) * 100 // len(criteria)
    st.metric("Resume Health Score", f"{score} / 100")

    missing = [key for key, filled in criteria.items() if not filled]
    if missing:
        st.warning("🚧 Sections to Improve:")
        st.write(", ".join(missing))
    else:
        st.success("✅ Your resume is complete and radiant!")

    # Save for Later
    st.markdown("---")
    st.header("💾 Save for Later")

    if st.button("Save My Resume Progress"):
        try:
            data = {key: st.session_state.get(key) for key in st.session_state.keys()}
            with open("soulskill_progress.json", "w") as f:
                json.dump(data, f)
            st.success("✅ Your progress has been saved! You can resume later by uploading this file.")
        except Exception as e:
            st.error(f"Failed to save progress: {e}")

    # Feedback
    st.markdown("---")
    st.header("💬 Feedback & Testimonials")

    feedback = st.text_area("Share your experience or suggestions")
    name = st.text_input("Your name (optional)")
    email = st.text_input("Your email (optional)")

    if st.button("Submit Feedback"):
        if feedback.strip():
            try:
                entry = {
                    "name": name,
                    "email": email,
                    "feedback": feedback
                }
                with open("soulskill_feedback.json", "a") as f:
                    f.write(json.dumps(entry) + "\n")
                st.success("🙏 Thank you for your feedback! Your voice helps SoulSkill grow.")
            except Exception as e:
                st.error(f"Failed to save feedback: {e}")
        else:
            st.warning("Please enter feedback before submitting.")
