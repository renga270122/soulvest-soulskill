import streamlit as st
from streamlit_lottie import st_lottie
import requests
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfkit
import tempfile
import fitz
from docx import Document
import base64

from stream_config import STREAM_OPTIONS
from education_config import DEGREE_OPTIONS, SCHOOL_PROGRAMS

def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

career_lottie = load_lottie("https://lottie.host/1c3a3b7e-2c9f-4e4a-9c3e-8c7d1f7b9e3f/animation.json")

st.set_page_config(page_title="SoulSkill", page_icon="✨", layout="centered")

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

if career_lottie:
    st_lottie(career_lottie, height=200)

st.markdown("---")
st.header("🪷 SoulSkill Ritual Mode")

if st.checkbox("Light your intention before you begin"):
    st.success("🕯️ Your intention is lit. Breathe in clarity, breathe out doubt.")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
    st.markdown("Affirmation: *I am worthy of every opportunity that aligns with my soul.*")

st.markdown("---")
st.header("📂 Upload Existing Resume")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    text = ""
    try:
        if uploaded_file.name.endswith(".pdf"):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        st.error(f"Error reading file: {e}")

    st.text_area("Extracted Resume Text", value=text, height=300)

    if st.button("✨ Auto-Fill Resume Fields"):
        if not text.strip():
            st.warning("No text extracted from the uploaded file.")
        else:
            lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
            full_text = " ".join(lines)

            summary_lines = [line for line in lines if re.search(r"(engineer|developer|lead|manager)", line.lower())]
            st.session_state.summary = " ".join(summary_lines[:2]) if summary_lines else "Experienced professional with a passion for growth and innovation."

            skill_keywords = [
                "python", "streamlit", "html", "css", "leadership", "communication", "project management", "sql", "data",
                "ai", "machine learning", "pyqt5", "gcc", "jira", "linux", "debugging", "ci/cd", "docker", "git"
            ]
            found_skills = sorted(set(word for word in skill_keywords if word.lower() in full_text.lower()))
            st.session_state.skills = ", ".join(found_skills).title() if found_skills else "Skills not detected"

            experience_lines = re.split(r'[•·]', full_text)
            experience_lines = [line.strip() for line in experience_lines if len(line.strip()) > 30]
            st.session_state.experience = "\n".join(experience_lines[:5]) if experience_lines else "Experience not detected"

            work_entries = []
            current_entry = {"title": "", "company": "", "duration": "", "responsibilities": ""}

            for line in lines:
                line_lower = line.lower()
                if any(role in line_lower for role in ["engineer", "developer", "manager", "consultant"]):
                    if current_entry["title"]:
                        work_entries.append(current_entry)
                        current_entry = {"title": "", "company": "", "duration": "", "responsibilities": ""}
                    current_entry["title"] = line.strip()
                elif re.search(r"\b(samsung|igate|solutions|labs|technologies|research)\b", line_lower):
                    current_entry["company"] = line.strip()
                elif re.search(r"\b\d{4}\b", line) and ("–" in line or "-" in line):
                    current_entry["duration"] = line.strip()
                elif line.startswith("·") or any(verb in line_lower for verb in ["developed", "built", "led", "created", "designed"]):
                    current_entry["responsibilities"] += line.strip() + " "

            if current_entry["title"]:
                work_entries.append(current_entry)

            st.session_state.work_entries = work_entries if work_entries else []

            st.success("All fields auto-filled! You can edit them in the next steps.")

if "template" not in st.session_state:
    st.session_state.template = "Soulful"

if st.session_state.step == 1:
    st.header("🎨 Choose Your Resume Style")
    st.session_state.template = st.selectbox("Select a template", ["Classic", "Modern", "Soulful"])
    st.button("Next", on_click=next_step)
# Step 2: Soulful Summary
elif st.session_state.step == 2:
    st.header("🌟 Soulful Summary")
    st.session_state.summary = st.text_area("Write your soulful summary", value=st.session_state.get("summary", ""))
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

# Step 3: Skills & Strengths
elif st.session_state.step == 3:
    st.header("🧠 Skills & Strengths")
    st.session_state.skills = st.text_area("List your skills and strengths", value=st.session_state.get("skills", ""))
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

# Step 4: Experience Highlights
elif st.session_state.step == 4:
    st.header("💼 Experience Highlights")
    st.session_state.experience = st.text_area("Share your key experiences", value=st.session_state.get("experience", ""))
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

# Step 5: Work History (Multiple Entries)
elif st.session_state.step == 5:
    st.header("📜 Work History")

    if "job_title" not in st.session_state:
        st.session_state.job_title = ""
        st.session_state.company_name = ""
        st.session_state.duration = ""
        st.session_state.responsibilities = ""

    st.session_state.job_title = st.text_input("Job Title", value=st.session_state.job_title)
    st.session_state.company_name = st.text_input("Company Name", value=st.session_state.company_name)
    st.session_state.duration = st.text_input("Duration (e.g., Jan 2020 – Dec 2023)", value=st.session_state.duration)
    st.session_state.responsibilities = st.text_area("Roles & Responsibilities", value=st.session_state.responsibilities)

    if st.button("➕ Add Entry"):
        st.session_state.work_entries.append({
            "title": st.session_state.job_title,
            "company": st.session_state.company_name,
            "duration": st.session_state.duration,
            "responsibilities": st.session_state.responsibilities
        })
        st.session_state.job_title = ""
        st.session_state.company_name = ""
        st.session_state.duration = ""
        st.session_state.responsibilities = ""
        st.success("Entry added!")

    if st.session_state.work_entries:
        st.markdown("### 🗂️ Your Work History")
        for i, entry in enumerate(st.session_state.work_entries):
            st.markdown(f"""
            **{entry['title']}**  
            {entry['company']} ({entry['duration']})  
            {entry['responsibilities']}
            """)

    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

# Step 6: Certifications & Courses
elif st.session_state.step == 6:
    st.header("🏅 Certifications & Courses")
    st.session_state.certifications = st.text_area("List your certifications and courses", value=st.session_state.get("certifications", ""))
    if not st.session_state.certifications:
        st.info("🧠 Tip: Add certifications like AWS, Scrum, or Python to boost your profile.")
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

# Step 7: Achievements
elif st.session_state.step == 7:
    st.header("🥇 Achievements")
    st.session_state.achievements = st.text_area("List your achievements and recognitions", value=st.session_state.get("achievements", ""))
    if not st.session_state.achievements:
        st.info("🏅 Tip: Mention awards, recognitions, or key milestones.")
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

# Step 8: Education
elif st.session_state.step == 8:
    st.header("🎓 Higher Education")

    st.session_state.degree = st.selectbox("Degree", DEGREE_OPTIONS, index=0)
    st.session_state.stream = st.selectbox("Stream / Specialization", STREAM_OPTIONS, index=0)
    st.session_state.university = st.text_input("University", value=st.session_state.get("university", ""))
    st.session_state.institution = st.text_input("Institution / College", value=st.session_state.get("institution", ""))
    st.session_state.grad_year = st.text_input("Graduation Year", value=st.session_state.get("grad_year", ""))
    st.session_state.grade = st.text_input("Percentage / Grade", value=st.session_state.get("grade", ""))

    st.markdown("### 🏫 School-Level Education (Optional)")
    st.session_state.school_program = st.selectbox("School Program", SCHOOL_PROGRAMS, index=0)
    st.session_state.school_name = st.text_input("School Name", value=st.session_state.get("school_name", ""))
    st.session_state.school_year = st.text_input("Year of Completion", value=st.session_state.get("school_year", ""))

    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)

# Step 9: Social Links
elif st.session_state.step == 9:
    st.header("🔗 Social Links")
    st.session_state.github = st.text_input("GitHub URL", value=st.session_state.get("github", ""))
    st.session_state.linkedin = st.text_input("LinkedIn URL", value=st.session_state.get("linkedin", ""))
    st.button("Back", on_click=prev_step)
    st.button("Next", on_click=next_step)
elif st.session_state.step == 10:
    st.header("📄 Resume Preview")

    style = st.session_state.template
    font = "Georgia" if style == "Classic" else "Verdana" if style == "Modern" else "Helvetica"

    # Profile Photo Upload
    st.markdown("### 🖼️ Upload Your Profile Photo (Optional)")
    photo = st.file_uploader("Upload a professional photo", type=["jpg", "jpeg", "png"])
    country = st.selectbox("Country you're applying in", ["India", "United States", "Europe", "Other"])

    photo_style = ""
    if photo:
        photo_bytes = photo.getvalue()
        encoded_photo = base64.b64encode(photo_bytes).decode()
        if country == "India":
            photo_style = "width:100px;border-radius:4px;border:1px solid #333;"
        elif country == "United States":
            photo_style = "width:120px;border-radius:50%;box-shadow:0 0 5px rgba(0,0,0,0.2);"
        elif country == "Europe":
            photo_style = "display:none;"
        else:
            photo_style = "width:100px;border-radius:8px;"
        photo_html = f"<img src='data:image/png;base64,{encoded_photo}' style='{photo_style}'/>"
    else:
        photo_html = ""

    # Clean & Optimize
    if st.button("🎯 Clean & Optimize Resume"):
        st.session_state.summary = re.sub(r"(Experienced professional.*?){2,}", r"\1", st.session_state.summary)
        st.session_state.experience = re.sub(r"(Experienced professional.*?){2,}", r"\1", st.session_state.experience)
        st.success("Resume content cleaned and optimized!")

    work_history_html = ""
    for entry in st.session_state.work_entries:
        work_history_html += f"<p><strong>{entry['title']}</strong><br>{entry['company']} ({entry['duration']})<br>{entry['responsibilities']}</p>"

    social_links_html = ""
    if st.session_state.get("github"):
        social_links_html += f"<a href='{st.session_state.github}' target='_blank'>🌐 GitHub</a> &nbsp;&nbsp;"
    if st.session_state.get("linkedin"):
        social_links_html += f"<a href='{st.session_state.linkedin}' target='_blank'>🔗 LinkedIn</a>"

    html_resume = f"""
    <html>
    <head>
    <style>
    body {{
        font-family: '{font}', sans-serif;
        background-color: #ffffff;
        padding: 40px;
        line-height: 1.6;
        color: #333333;
    }}
    h3 {{
        color: #222;
        border-bottom: 1px solid #ccc;
        padding-bottom: 5px;
    }}
    p {{
        margin: 10px 0;
    }}
    </style>
    </head>
    <body>
    {photo_html}
    <h3>🌟 Summary</h3>
    <p>{st.session_state.get("summary", "")}</p>
    <h3>🧠 Skills</h3>
    <p>{st.session_state.get("skills", "")}</p>
    <h3>💼 Experience Highlights</h3>
    <p>{st.session_state.get("experience", "")}</p>
    <h3>📜 Work History</h3>
    {work_history_html}
    <h3>🎓 Higher Education</h3>
    <p>
    {st.session_state.get("degree", "")}<br>
    Stream: {st.session_state.get("stream", "")}<br>
    {st.session_state.get("university", "")}<br>
    {st.session_state.get("institution", "")}<br>
    Graduation Year: {st.session_state.get("grad_year", "")}<br>
    Grade: {st.session_state.get("grade", "")}
    </p>
    <h3>🏫 School Education</h3>
    <p>
    Program: {st.session_state.get("school_program", "")}<br>
    School: {st.session_state.get("school_name", "")}<br>
    Year of Completion: {st.session_state.get("school_year", "")}
    </p>
    <h3>🏅 Certifications & Courses</h3>
    <p>{st.session_state.get("certifications", "")}</p>
    <h3>🥇 Achievements</h3>
    <p>{st.session_state.get("achievements", "")}</p>
    <h3>🔗 Social Links</h3>
    <p>{social_links_html}</p>
    </body>
    </html>
    """

    st.markdown(html_resume, unsafe_allow_html=True)

    try:
        config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None
        }
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdfkit.from_string(html_resume, tmp.name, options=options, configuration=config)
            st.download_button("📥 Resume Ready: Click to Save", data=open(tmp.name, "rb").read(), file_name="SoulSkill_Resume.pdf")
    except Exception as e:
        st.error(f"PDF generation failed: {e}")

    st.button("Back", on_click=prev_step)

    # Resume Health Score
    st.markdown("---")
    st.header("📊 Resume Health Score")

    score = 0
    feedback = []

    if len(st.session_state.get("summary", "")) >= 50:
        score += 20
    else:
        feedback.append("📝 Add a stronger summary (2–3 lines).")

    if len(st.session_state.get("skills", "").split(",")) >= 5:
        score += 20
    else:
        feedback.append("🧠 Add more technical and soft skills.")

    if len(st.session_state.get("experience", "").split("\n")) >= 3:
        score += 20
    else:
        feedback.append("💼 Add more experience highlights.")

    if st.session_state.work_entries:
        score += 20
    else:
        feedback.append("📜 Add at least one work history entry.")

    if st.session_state.get("certifications") or st.session_state.get("achievements"):
        score += 20
    else:
        feedback.append("🏅 Add certifications or achievements.")

    st.metric("Resume Health Score", f"{score} / 100")

    if feedback:
        st.warning("Suggestions to improve your resume:")
        for tip in feedback:
            st.markdown(f"- {tip}")
    else:
        st.success("✅ Your resume looks strong and ready to apply!")

    # ATS Optimizer
    st.markdown("---")
    st.header("🧠 ATS Optimizer")

    job_desc = st.text_area("📄 Paste Job Description")
    resume_text = f"{st.session_state.get('summary', '')} {st.session_state.get('skills', '')} {st.session_state.get('experience', '')} {st.session_state.get('certifications', '')} {st.session_state.get('achievements', '')} " + " ".join([f"{e['title']} {e['company']} {e['responsibilities']}" for e in st.session_state.work_entries])

    if st.button("🔍 Analyze ATS Match"):
        if job_desc and resume_text:
            try:
                vectorizer = CountVectorizer().fit_transform([job_desc, resume_text])
                score = cosine_similarity(vectorizer)[0][1]
                st.metric("ATS Match Score", f"{round(score * 100)} / 100")

                job_keywords = set(re.findall(r'\b\w+\b', job_desc.lower()))
                resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
                missing_keywords = job_keywords - resume_words

                st.warning("🧠 Missing Keywords:")
                st.write(", ".join(sorted(missing_keywords)))
            except Exception as e:
                st.error(f"ATS analysis failed: {e}")
        else:
            st.error("Please paste both job description and resume.")

    # Cover Letter Generator
    st.markdown("---")
    st.header("💌 Cover Letter Generator")

    tone = st.selectbox("Choose your tone", ["Confident", "Humble", "Visionary"])

    if st.button("Generate Cover Letter"):
        work_lines = "\n".join([
            f"{e['title']} at {e['company']} ({e['duration']})"
            for e in st.session_state.work_entries
        ])

        cover_letter = f"""
    Dear Hiring Manager,

    I am writing to express my interest in the role at your esteemed organization. With a background in {st.session_state.get("experience", "")}, and a passion for {st.session_state.get("skills", "")}, I believe I bring both skill and soul to the opportunity.

    My journey has been shaped by roles such as:
    {work_lines}

    I am excited to contribute with {tone.lower()} energy and a commitment to growth. I would welcome the opportunity to discuss how my experience and values align with your team’s mission.

    With gratitude,  
    Renganathan
        """.strip()

    st.text_area("Your Cover Letter", value=cover_letter, height=300)


    # Final Dynamic Job Matching Dashboard
    st.markdown("---")
    st.header("🔍 Job Matching Dashboard")

    st.markdown("### ✨ Explore Real-Time Listings")
    st.markdown("- [LinkedIn Jobs](https://www.linkedin.com/jobs/)")
    st.markdown("- [Naukri Jobs](https://www.naukri.com/)")
    st.markdown("- [Indeed Jobs](https://www.indeed.com/q-python-developer-jobs.html)")
    st.markdown("- [Glassdoor Jobs](https://www.glassdoor.co.in/Job/index.htm)")
    st.markdown("- [Monster India](https://www.monsterindia.com/)")

    st.info("These portals update in real-time. Use your SoulSkill resume to apply confidently.")
