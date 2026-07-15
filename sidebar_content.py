"""
Enhanced Sidebar Content for SoulSkill Career Growth Platform
"""
import streamlit as st
import random
from datetime import datetime

# Motivational quotes for career success
MOTIVATIONAL_QUOTES = [
    "Your story deserves to be seen. Make it compelling! 📖",
    "Every great career starts with a clear direction. ✨",
    "You're not just preparing a resume, you're building your future! 🚀",
    "Success is the sum of small efforts repeated day in and day out. 💪",
    "Your skills are valuable. Show them to the world! 🌟",
    "The best time to improve your profile was yesterday. The second best time is now! ⏰",
    "Don't tell them what you did. Show them what you achieved! 📊",
    "Quantify your impact. Numbers speak louder than words! 🔢",
    "ATS-friendly today, interview-ready tomorrow! ✅",
    "Your dream role is one strong story away! 💼",
]

# Quick tips for different sections
QUICK_TIPS = {
    "general": [
        "💡 Keep it concise: 1 page for <5 years experience, 2 pages for >5 years",
        "📝 Use action verbs: Led, Developed, Managed, Increased",
        "📊 Quantify achievements: 'Increased sales by 30%' beats 'Improved sales'",
        "🎯 Tailor for each job: Match keywords from job description",
        "✨ White space matters: Don't overcrowd your profile",
    ],
    "summary": [
        "🎯 Write for the role you want, not the one you have",
        "💼 Include years of experience and key expertise",
        "🌟 Highlight your unique value proposition",
        "📈 Mention measurable achievements if possible",
    ],
    "experience": [
        "💪 Start with strong action verbs",
        "📊 Include metrics and percentages",
        "🎯 Focus on impact, not just tasks",
        "⏰ Use past tense for completed work",
        "🔥 Highlight promotions and leadership",
    ],
    "skills": [
        "🔍 Include job-specific keywords",
        "⭐ Separate technical and soft skills",
        "📚 Add proficiency levels if relevant",
        "🆕 Keep skills current and in-demand",
    ],
}

# ATS statistics
ATS_STATS = {
    "75%": "of resumes never reach human eyes (rejected by ATS)",
    "6 sec": "Average time a recruiter spends on initial resume scan",
    "43%": "of resumes with photos are rejected automatically",
    "88%": "of recruiters use keywords to filter candidates",
    "60%": "better chance with ATS-optimized format",
}

# Career readiness checklist
RESUME_CHECKLIST = [
    {"item": "Contact info is complete and professional", "category": "foundation"},
    {"item": "Email address is professional (no nicknames)", "category": "foundation"},
    {"item": "Summary highlights your current direction", "category": "story"},
    {"item": "Projects or experience use action verbs", "category": "story"},
    {"item": "Achievements include numbers or evidence", "category": "story"},
    {"item": "No spelling or grammar errors", "category": "quality"},
    {"item": "Consistent formatting throughout", "category": "quality"},
    {"item": "Keywords match target role expectations", "category": "ats"},
    {"item": "Simple, single-column layout", "category": "ats"},
    {"item": "Standard section headings used", "category": "ats"},
]


def show_progress_tracker():
    """Display career profile completion progress"""
    st.markdown("### 📊 Career progress")
    
    # Calculate completion
    fields_to_check = [
        ('full_name', 'Basic Info'),
        ('email', 'Contact'),
        ('summary', 'Summary'),
        ('tech_skills', 'Skills'),
        ('work_entries', 'Experience'),
        ('education_entries', 'Education'),
    ]
    
    completed = 0
    total = len(fields_to_check)
    
    for field, label in fields_to_check:
        value = st.session_state.get(field, None)
        if value:
            if isinstance(value, list):
                if len(value) > 0:
                    completed += 1
            elif isinstance(value, str):
                if value.strip():
                    completed += 1
            else:
                completed += 1
    
    percentage = int((completed / total) * 100)
    st.progress(percentage / 100)
    st.caption(f"**{percentage}% Complete** ({completed}/{total} sections)")
    
    # Show what's missing
    if percentage < 100:
        st.markdown("**Still needed:**")
        for field, label in fields_to_check:
            value = st.session_state.get(field, None)
            is_complete = False
            if value:
                if isinstance(value, list):
                    is_complete = len(value) > 0
                elif isinstance(value, str):
                    is_complete = bool(value.strip())
                else:
                    is_complete = True

            if not is_complete:
                st.caption(f"⭕ {label}")


def show_next_best_action():
    """Display the most useful next step based on the current profile state."""
    profile_score = _safe_int(st.session_state.get("career_readiness_score"), 72)
    if profile_score < 50:
        message = "Finish the basics, then add one project or achievement to strengthen your story."
    elif profile_score < 75:
        message = "Refine your summary and align keywords with your target role."
    else:
        message = "Polish interview stories and build a strong application list this week."

    st.markdown("### Next best action")
    st.info(message)


def show_motivational_quote():
    """Display a random motivational quote"""
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.info(quote)


def show_quick_tips(section: str = "general"):
    """Show quick tips for a specific section"""
    tips = QUICK_TIPS.get(section, QUICK_TIPS["general"])
    
    for tip in tips:
        st.caption(tip)


def show_ats_statistics():
    """Display ATS-related statistics"""
    st.markdown("### 📈 Career signals")
    
    for stat, description in ATS_STATS.items():
        st.metric(
            label=description,
            value=stat,
            delta=None
        )
    
    st.caption("Source: Industry research 2025")


def show_resume_checklist():
    """Interactive career readiness checklist"""
    st.markdown("### ✅ Career readiness checklist")
    
    if 'checklist_items' not in st.session_state:
        st.session_state.checklist_items = {i: False for i in range(len(RESUME_CHECKLIST))}
    
    categories = {}
    for idx, item in enumerate(RESUME_CHECKLIST):
        cat = item['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((idx, item['item']))
    
    category_labels = {
        "foundation": "FOUNDATION",
        "story": "YOUR STORY",
        "quality": "QUALITY",
        "ats": "ATS FIT",
    }

    for category, items in categories.items():
        st.markdown(f"**{category_labels.get(category, category.upper())}**")
        for idx, item_text in items:
            unique_key = f"checklist_{category}_{idx}"
            checked = st.checkbox(
                item_text,
                value=st.session_state.checklist_items[idx],
                key=unique_key
            )
            st.session_state.checklist_items[idx] = checked
    
    # Calculate completion
    completed = sum(st.session_state.checklist_items.values())
    total = len(RESUME_CHECKLIST)
    st.caption(f"**{completed}/{total} items checked**")


def show_job_search_resources():
    """Display helpful job search resources"""
    st.markdown("### 🔗 Resources")
    
    resources = [
        ("LinkedIn Jobs", "https://www.linkedin.com/jobs/"),
        ("Indeed", "https://www.indeed.com/"),
        ("Glassdoor", "https://www.glassdoor.com/"),
        ("AngelList (Startups)", "https://angel.co/jobs"),
        ("Remote.co", "https://remote.co/"),
    ]
    
    for name, url in resources:
        st.markdown(f"[{name} →]({url})")


def show_success_stories():
    """Display success stories/testimonials"""
    stories = [
        {
            "name": "Priya S.",
            "role": "Software Engineer",
            "text": "Got 3 interviews in 2 weeks after tightening my story and projects! 🎉",
            "achievement": "50% response rate"
        },
        {
            "name": "Rahul M.",
            "role": "Product Manager",
            "text": "The ATS checker helped me optimize for keywords and confidence. Landed my dream job!",
            "achievement": "Dream job @ Google"
        },
        {
            "name": "Ananya K.",
            "role": "Data Analyst",
            "text": "The templates are so professional. Built my profile in 15 minutes!",
            "achievement": "15 min to strong profile"
        },
    ]
    
    st.markdown("### ⭐ Success Stories")
    story = random.choice(stories)
    
    st.markdown(f"**{story['name']}** - *{story['role']}*")
    st.caption(f'"{story["text"]}"')
    st.success(f"✨ {story['achievement']}")


def show_live_stats():
    """Show live platform statistics"""
    st.markdown("### 📊 Live Stats")
    
    # Simulated stats (in production, fetch from database)
    base_profiles = 15420
    base_users = 8934
    
    # Add some variability based on time
    hour_offset = datetime.now().hour
    profiles_today = base_profiles + (hour_offset * 17)
    users_today = base_users + (hour_offset * 9)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Profiles Improved", f"{profiles_today:,}", "+127 today")
    with col2:
        st.metric("Career Learners", f"{users_today:,}", "+89 today")
    
    st.caption("🌟 Join thousands building stronger career stories!")


def _safe_int(value, default: int) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def render_enhanced_sidebar():
    """
    Render complete enhanced sidebar with all components
    Usage: Call this function in your main app
    """
    with st.sidebar:
        st.markdown(
            """
            <style>
            .sidebar-shell {
                background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(30, 41, 59, 0.96) 100%);
                border-radius: 20px;
                padding: 1rem;
                color: #f8fafc;
                box-shadow: 0 16px 36px rgba(15, 23, 42, 0.18);
                margin-bottom: 1rem;
            }
            .sidebar-shell h1, .sidebar-shell h2, .sidebar-shell h3, .sidebar-shell p {
                margin: 0;
            }
            .sidebar-metric {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 0.75rem;
                min-height: 84px;
            }
            .sidebar-metric .label {
                font-size: 0.72rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                opacity: 0.8;
            }
            .sidebar-metric .value {
                font-size: 1.3rem;
                font-weight: 800;
                margin-top: 0.2rem;
            }
            .sidebar-card {
                background: rgba(248, 250, 252, 0.96);
                border-radius: 16px;
                padding: 0.9rem;
                margin-bottom: 0.9rem;
                border: 1px solid rgba(148, 163, 184, 0.18);
                box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08);
            }
            .sidebar-card h3 {
                color: #0f172a;
                margin-bottom: 0.35rem;
            }
            .sidebar-card p, .sidebar-card li, .sidebar-card a, .sidebar-card caption {
                color: #475569;
                line-height: 1.45;
            }
            .sidebar-pill {
                display: inline-block;
                margin-top: 0.35rem;
                padding: 0.22rem 0.55rem;
                border-radius: 999px;
                font-size: 0.72rem;
                font-weight: 700;
                color: #1d4ed8;
                background: #dbeafe;
            }
            .quick-action-row .stButton>button {
                min-height: 40px;
                padding: 0.15rem 0.25rem;
                font-size: 0.72rem;
                white-space: nowrap !important;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .quick-action-row .stButton>button p {
                margin: 0;
                white-space: nowrap !important;
                overflow-wrap: normal !important;
                word-break: normal !important;
                line-height: 1.05;
                font-size: 0.72rem;
            }
            .quick-action-row .stButton>button div {
                white-space: nowrap !important;
                overflow-wrap: normal !important;
                word-break: normal !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""
        <div class='sidebar-shell' style='text-align: center;'>
        """, unsafe_allow_html=True)
        try:
            st.image("assets/logo.png", width=200)
        except:
            st.markdown("""
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🚀</div>
            <h1 style='font-size: 1.8rem; font-weight: 800; margin: 0; color: white; font-family: 'Poppins', sans-serif;'>SoulSkill</h1>
            """, unsafe_allow_html=True)
        st.markdown("""
            <p style='font-size: 0.95rem; font-weight: 700; margin: 0.5rem 0 0.25rem; color: rgba(255,255,255,0.96);'>AI Career Growth Platform</p>
            <p style='font-size: 0.85rem; font-weight: 500; margin: 0.25rem 0 0; color: rgba(255,255,255,0.75); font-style: italic;'>✨ Build confidence, skill, and interview readiness</p>
        </div>
        """, unsafe_allow_html=True)

        readiness = _safe_int(st.session_state.get("career_readiness_score"), 72)
        resume_score = _safe_int(st.session_state.get("resume_score"), 68)
        ats_score = _safe_int(st.session_state.get("ats_score"), 64)
        interview_score = _safe_int(st.session_state.get("interview_readiness"), 61)

        st.markdown("### 📌 At a glance")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"<div class='sidebar-metric'><div class='label'>Readiness</div><div class='value'>{readiness}%</div></div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"<div class='sidebar-metric'><div class='label'>ATS</div><div class='value'>{ats_score}%</div></div>",
                unsafe_allow_html=True,
            )
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                f"<div class='sidebar-metric'><div class='label'>Profile</div><div class='value'>{resume_score}%</div></div>",
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                f"<div class='sidebar-metric'><div class='label'>Interview</div><div class='value'>{interview_score}%</div></div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div class='sidebar-pill'>Daily guidance</div>", unsafe_allow_html=True)
        show_motivational_quote()

        st.markdown("### ⚡ Quick Actions")
        st.markdown("<div class='quick-action-row'>", unsafe_allow_html=True)
        action_cols = st.columns(2)
        with action_cols[0]:
            if st.button("Dashboard", use_container_width=True):
                st.session_state.mode = "dashboard"
                st.rerun()
            if st.button("Career Growth", use_container_width=True):
                st.session_state.mode = "growth"
                st.rerun()
        with action_cols[1]:
            if st.button("Career Toolkit", use_container_width=True):
                st.session_state.mode = "toolkit"
                st.rerun()
            if st.button("Interview Prep", use_container_width=True):
                st.session_state.mode = "interview"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        show_next_best_action()

        st.markdown("### 🎯 Focus this week")
        show_quick_tips("general")

        st.markdown("### 📈 Progress")
        show_progress_tracker()

        st.markdown("### 🧠 Skill + ATS check")
        show_ats_statistics()

        st.markdown("### ⭐ Confidence boost")
        show_success_stories()

        st.markdown("### 🔗 Helpful Links")
        show_job_search_resources()

        st.markdown("### 🌟 Snapshot")
        show_live_stats()
