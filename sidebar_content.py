"""
Enhanced Sidebar Content for SoulSkill Resume Builder
"""
import streamlit as st
import random
from datetime import datetime

# Motivational quotes for career success
MOTIVATIONAL_QUOTES = [
    "Your resume is your story. Make it compelling! 📖",
    "Every great career starts with a great resume. ✨",
    "You're not just building a resume, you're building your future! 🚀",
    "Success is the sum of small efforts repeated day in and day out. 💪",
    "Your skills are valuable. Show them to the world! 🌟",
    "The best time to update your resume was yesterday. The second best time is now! ⏰",
    "Don't tell them what you did. Show them what you achieved! 📊",
    "Quantify your impact. Numbers speak louder than words! 🔢",
    "ATS-friendly today, interview-ready tomorrow! ✅",
    "Your dream job is one great resume away! 💼",
]

# Quick tips for different sections
QUICK_TIPS = {
    "general": [
        "💡 Keep it concise: 1 page for <5 years experience, 2 pages for >5 years",
        "📝 Use action verbs: Led, Developed, Managed, Increased",
        "📊 Quantify achievements: 'Increased sales by 30%' beats 'Improved sales'",
        "🎯 Tailor for each job: Match keywords from job description",
        "✨ White space matters: Don't overcrowd your resume",
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

# Resume checklist
RESUME_CHECKLIST = [
    {"item": "Contact info is complete and professional", "category": "basics"},
    {"item": "Email address is professional (no nicknames)", "category": "basics"},
    {"item": "Summary highlights key achievements", "category": "content"},
    {"item": "Work experience uses action verbs", "category": "content"},
    {"item": "Achievements include numbers/metrics", "category": "content"},
    {"item": "No spelling or grammar errors", "category": "quality"},
    {"item": "Consistent formatting throughout", "category": "quality"},
    {"item": "Keywords match target job description", "category": "ats"},
    {"item": "Simple, single-column layout", "category": "ats"},
    {"item": "Standard section headings used", "category": "ats"},
]


def show_progress_tracker():
    """Display resume completion progress"""
    st.markdown("### 📊 Your Progress")
    
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
    st.markdown("### 📈 Resume Stats")
    
    for stat, description in ATS_STATS.items():
        st.metric(
            label=description,
            value=stat,
            delta=None
        )
    
    st.caption("Source: Industry research 2025")


def show_resume_checklist():
    """Interactive resume checklist"""
    st.markdown("### ✅ Resume Checklist")
    
    if 'checklist_items' not in st.session_state:
        st.session_state.checklist_items = {i: False for i in range(len(RESUME_CHECKLIST))}
    
    categories = {}
    for idx, item in enumerate(RESUME_CHECKLIST):
        cat = item['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((idx, item['item']))
    
    for category, items in categories.items():
        st.markdown(f"**{category.upper()}**")
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
            "text": "Got 3 interviews in 2 weeks with my new resume! 🎉",
            "achievement": "50% response rate"
        },
        {
            "name": "Rahul M.",
            "role": "Product Manager",
            "text": "The ATS checker helped me optimize for keywords. Landed my dream job!",
            "achievement": "Dream job @ Google"
        },
        {
            "name": "Ananya K.",
            "role": "Data Analyst",
            "text": "The templates are so professional. Built my resume in 15 minutes!",
            "achievement": "15 min to perfect resume"
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
    base_resumes = 15420
    base_users = 8934
    
    # Add some variability based on time
    hour_offset = datetime.now().hour
    resumes_today = base_resumes + (hour_offset * 17)
    users_today = base_users + (hour_offset * 9)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Resumes Built", f"{resumes_today:,}", "+127 today")
    with col2:
        st.metric("Happy Users", f"{users_today:,}", "+89 today")
    
    st.caption("🌟 Join thousands building career-winning resumes!")


def render_enhanced_sidebar():
    """
    Render complete enhanced sidebar with all components
    Usage: Call this function in your main app
    """
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin-bottom: 1rem;'>
        """, unsafe_allow_html=True)
        try:
            st.image("assets/logo.png", use_column_width=True, width=200)
        except:
            st.markdown("""
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🚀</div>
            <h1 style='font-size: 1.8rem; font-weight: 800; margin: 0; color: white; font-family: 'Poppins', sans-serif;'>SoulSkill</h1>
            """, unsafe_allow_html=True)
        st.markdown("""
            <p style='font-size: 0.95rem; font-weight: 600; margin: 0.5rem 0; color: rgba(255,255,255,0.9);'>AI-Powered Resume Builder</p>
            <p style='font-size: 0.85rem; font-weight: 500; margin: 0.25rem 0; color: rgba(255,255,255,0.75); font-style: italic;'>✨ Build Your Future in Minutes</p>
        </div>
        """, unsafe_allow_html=True)
