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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Config files
from stream_config import STREAM_OPTIONS
from education_config import DEGREE_OPTIONS, SCHOOL_PROGRAMS
from template_config import TEMPLATES

st.set_page_config(page_title="SoulSkill", page_icon="✨", layout="centered")

def sanitize_text(text):
    return text.encode("utf-8", errors="ignore").decode("utf-8").replace("â", "-").replace("ðŸ", "").replace("ï", "").replace("ÕŸ", "").replace("ðÝŽ“", "")

if "step" not in st.session_state:
    st.session_state.step = 1
if "work_entries" not in st.session_state:
    st.session_state.work_entries = []

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

st.title("✨ SoulSkill: Resume Builder")
st.subheader("Empower your career with clarity and soul")
if st.session_state.step == 1:
    st.header("🎨 Choose Your Resume Style")

    template_names = list(TEMPLATES.keys())
    selected_template = st.selectbox("Select a template", template_names)
    st.session_state.template = selected_template

    font = TEMPLATES[selected_template]['font']
    color = TEMPLATES[selected_template]['color']

    st.markdown(f"**Font:** `{font}`")
    st.markdown(f"<div style='width:100px;height:20px;background-color:{color};border-radius:4px;border:1px solid #ccc;'></div>", unsafe_allow_html=True)

    layout_choice = st.radio("Choose resume layout", ["Single Column", "Two Column"])
    st.session_state.layout = layout_choice

    st.markdown("---")
    st.markdown("### 🖼️ Live Resume Preview")

    sample_photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Sample_User_Icon.png/240px-Sample_User_Icon.png"
    photo_html = f"<img src='{sample_photo_url}' style='width:100px;border-radius:8px;margin-bottom:10px;'/>"

    if layout_choice == "Single Column":
        preview_html = f"""
        <html><body style="font-family:{font};color:{color};padding:20px;">
        {photo_html}
        <h2>John Doe</h2>
        <p><strong>Software Engineer</strong></p>
        <h3>Summary</h3><p>Creative and detail-oriented engineer...</p>
        <h3>Skills</h3><p>Python, Streamlit, GitHub...</p>
        <h3>Education</h3><p>B.Tech in CSE, VTU</p>
        <h3>Portfolio</h3><p><a href='https://soulvest.ai'>Soulvest.ai</a></p>
        <img src='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=https://soulvest.ai'/>
        </body></html>
        """
    else:
        preview_html = f"""
        <html><body style="font-family:{font};color:{color};padding:20px;">
        <div style="display:flex;gap:30px;">
        <div style="width:35%;">{photo_html}<h3>Contact</h3><p>hello@soulskill.ai</p></div>
        <div style="width:65%;"><h2>John Doe</h2><p><strong>Software Engineer</strong></p>
        <h3>Summary</h3><p>Creative and detail-oriented engineer...</p></div>
        </div>
        </body></html>
        """

    st.markdown(preview_html, unsafe_allow_html=True)
    st.button("Next", on_click=next_step)
elif st.session_state.step == 2:
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
