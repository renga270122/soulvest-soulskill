# app.py - Soulvest AI Resume Builder - Enterprise-Grade Resume Creation
# Advanced AI • Premium Templates • ATS Optimization • Complete Career Toolkit
import streamlit as st
import base64
import tempfile
import json
import os
from datetime import datetime
import time

# Import configurations
from template_config import TEMPLATES, INDIAN_TEMPLATES
from industry_config import INDUSTRY_OPTIONS, INDUSTRY_KEYWORDS, MAJOR_INDIAN_CITIES, INDIAN_STATES
from stream_config import STREAM_OPTIONS
from education_config import DEGREE_OPTIONS

# Import AI and resume generation modules
from ai_assistant import AIResumeAssistant, ATSOptimizer
from ai_advanced import AdvancedAIAssistant, ResumeScoring
from ats_optimizer_pro import EnterpriseATSOptimizer
from premium_templates import PREMIUM_TEMPLATES, get_template_recommendations
from export_manager import ExportManager
from resume_generator import generate_resume_html
from advanced_features import (
    ResumeImporter, QRCodeGenerator, SpellChecker, 
    ResumeVersionControl, EmailTemplates, KeywordHighlighter, 
    ResumeLengthOptimizer
)
from job_examples import (
    PROFESSIONAL_SUMMARIES, WORK_EXPERIENCE_EXAMPLES, SKILLS_EXAMPLES,
    PROJECT_EXAMPLES, get_examples_for_role, get_all_job_roles
)

# Try to import PDF generation
try:
    import pdfkit
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="Soulvest AI Resume Builder - Enterprise-Grade Career Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Note: PWA features (manifest.json, service-worker.js) are configured separately
# SEO meta tags are handled by Streamlit Cloud deployment settings

# Custom CSS for modern, mobile-responsive design with motivating theme
st.markdown("""
<style>
    .main {
        padding: 1rem;
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 50%, #f093fb15 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.75rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    .ai-button>button {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%) !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .ats-score-excellent {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    .ats-score-good {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    .ats-score-poor {
        background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    h1 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .tip-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .motivational-quote {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        text-align: center;
        font-size: 1.1rem;
        font-style: italic;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    .success-story {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #00b894;
    }
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-top: 4px solid #667eea;
    }
    @media (max-width: 768px) {
        .main {padding: 0.5rem;}
        h1 {font-size: 1.8rem;}
    }
    
    /* Dark Mode Styles */
    [data-theme="dark"] .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e0e0;
    }
    [data-theme="dark"] .stButton>button {
        background: linear-gradient(90deg, #0f3460 0%, #533483 100%);
    }
    [data-theme="dark"] .feature-card {
        background: #1e1e2e;
        color: #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5);
        border-left-color: #0f3460;
    }
    [data-theme="dark"] .tip-box {
        background: #2a2a1a;
        border-left-color: #666600;
        color: #e0e0e0;
    }
    [data-theme="dark"] .metric-card {
        background: linear-gradient(135deg, #0f3460 0%, #533483 100%);
    }
    [data-theme="dark"] .stTextInput {
        background-color: #1e1e2e;
        color: #e0e0e0;
    }
    [data-theme="dark"] .stTextArea {
        background-color: #1e1e2e;
        color: #e0e0e0;
    }
    [data-theme="dark"] .stSelectbox {
        background-color: #1e1e2e;
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize AI Assistant
def get_ai_assistant():
    api_key = None
    # Try st.secrets first (works in both local and cloud)
    try:
        if 'GOOGLE_API_KEY' in st.secrets:
            api_key = st.secrets['GOOGLE_API_KEY']
    except Exception:
        pass
    # Fallback to environment variable
    if api_key is None:
        api_key = os.getenv('GOOGLE_API_KEY')
    return AIResumeAssistant(api_key)

def get_advanced_ai():
    api_key = None
    # Try st.secrets first (works in both local and cloud)
    try:
        if 'GOOGLE_API_KEY' in st.secrets:
            api_key = st.secrets['GOOGLE_API_KEY']
    except Exception:
        pass
    # Fallback to environment variable
    if api_key is None:
        api_key = os.getenv('GOOGLE_API_KEY')
    return AdvancedAIAssistant(api_key)

# Check if we need to reinitialize AI (in case API key was added after first load)
if 'ai_assistant' not in st.session_state or 'force_ai_reload' in st.session_state:
    if 'force_ai_reload' in st.session_state:
        del st.session_state.force_ai_reload
    st.session_state.ai_assistant = get_ai_assistant()
    st.session_state.advanced_ai = get_advanced_ai()

ai_assistant = st.session_state.ai_assistant
advanced_ai = st.session_state.advanced_ai

# Initialize Session State
def init_session_state():
    defaults = {
        'step': 0,
        'profile_type': None,
        'work_entries': [],
        'education_entries': [],
        'certification_entries': [],
        'project_entries': [],
        'language_entries': [],
        'ats_score': None,
        'job_description': '',
        'ai_enabled': ai_assistant.enabled,
        'progress_checked': False,
        'show_restore': False,
        'last_saved_time': '',
        'theme': 'light'  # Dark mode support: 'light' or 'dark'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Auto-save functionality
def auto_save_progress():
    """Auto-save resume progress to local storage"""
    try:
        # Create a serializable copy of session state
        save_data = {
            'last_saved': datetime.now().isoformat(),
            'step': st.session_state.get('step', 0),
            'full_name': st.session_state.get('full_name', ''),
            'email': st.session_state.get('email', ''),
            'phone': st.session_state.get('phone', ''),
            'city': st.session_state.get('city', ''),
            'state': st.session_state.get('state', ''),
            'linkedin': st.session_state.get('linkedin', ''),
            'github': st.session_state.get('github', ''),
            'portfolio': st.session_state.get('portfolio', ''),
            'profile_type': st.session_state.get('profile_type', ''),
            'industry': st.session_state.get('industry', ''),
            'job_title_target': st.session_state.get('job_title_target', ''),
            'template': st.session_state.get('template', ''),
            'summary': st.session_state.get('summary', ''),
            'tech_skills': st.session_state.get('tech_skills', ''),
            'soft_skills': st.session_state.get('soft_skills', ''),
            'work_entries': st.session_state.get('work_entries', []),
            'education_entries': st.session_state.get('education_entries', []),
            'certification_entries': st.session_state.get('certification_entries', []),
            'project_entries': st.session_state.get('project_entries', []),
            'language_entries': st.session_state.get('language_entries', []),
        }
        
        # Save to file
        with open("soulskill_autosave.json", "w", encoding='utf-8') as f:
            json.dump(save_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Auto-save error: {e}")
        return False

def load_saved_progress():
    """Load saved progress if available"""
    try:
        if os.path.exists("soulskill_autosave.json"):
            with open("soulskill_autosave.json", "r", encoding='utf-8') as f:
                saved_data = json.load(f)
            
            # Restore session state
            for key, value in saved_data.items():
                if key != 'last_saved' and key in st.session_state:
                    st.session_state[key] = value
            
            return saved_data.get('last_saved', '')
    except Exception as e:
        print(f"Load error: {e}")
    return None

# Check for saved progress on startup
if st.session_state.step == 0 and not st.session_state.get('progress_checked'):
    st.session_state.progress_checked = True
    last_saved = load_saved_progress()
    if last_saved:
        # Show restore option in sidebar
        st.session_state.show_restore = True
        st.session_state.last_saved_time = last_saved

# Navigation functions
def next_step():
    st.session_state.step += 1
    auto_save_progress()  # Auto-save on navigation

def prev_step():
    st.session_state.step -= 1
    auto_save_progress()  # Auto-save on navigation

def goto_step(step_num):
    st.session_state.step = step_num
    auto_save_progress()  # Auto-save on navigation

# Sidebar Navigation
with st.sidebar:
    # SOULVEST Logo
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
            <h1 style='margin: 0; font-size: 2rem;'>✨</h1>
            <h2 style='margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 700;'>SOULVEST</h2>
            <p style='margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>AI Resume Builder</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; font-size: 0.85rem; color: #666;'>🚀 Your Career, Supercharged</p>", unsafe_allow_html=True)
    
    # Show restore progress option
    if st.session_state.get('show_restore', False):
        with st.expander("💾 Resume Saved Progress", expanded=True):
            last_saved = st.session_state.get('last_saved_time', '')
            try:
                saved_time = datetime.fromisoformat(last_saved)
                time_str = saved_time.strftime("%b %d, %Y %I:%M %p")
            except:
                time_str = "Earlier"
            
            st.info(f"Last saved: {time_str}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📂 Resume", use_container_width=True):
                    load_saved_progress()
                    st.session_state.show_restore = False
                    st.rerun()
            with col2:
                if st.button("🔄 Start Fresh", use_container_width=True):
                    # Clear saved progress
                    if os.path.exists("soulskill_autosave.json"):
                        os.remove("soulskill_autosave.json")
                    st.session_state.show_restore = False
                    st.rerun()
        st.markdown("---")
    
    if st.session_state.ai_enabled:
        st.success("✨ AI Features: ACTIVE")
    else:
        st.warning("⚠️ AI Features: Offline Mode")
        with st.expander("Enable AI Features"):
            st.write("To enable AI features, add your Google Gemini API key:")
            st.code("GOOGLE_API_KEY=your_key_here")
            st.caption("[Get free API key](https://makersuite.google.com/app/apikey)")
            
            # Debug info
            if st.button("🔄 Reload API Key"):
                st.session_state.force_ai_reload = True
                st.rerun()
            
            # Show debug info
            has_secret = 'GOOGLE_API_KEY' in st.secrets if hasattr(st, 'secrets') else False
            has_env = os.getenv('GOOGLE_API_KEY') is not None
            st.caption(f"Debug: secrets.toml={has_secret}, env={has_env}")
    
    st.markdown("---")
    
    if st.session_state.step > 0:
        progress = (st.session_state.step / 11) * 100
        st.progress(progress / 100)
        st.caption(f"Progress: {int(progress)}%")
        
        # Show auto-save status
        if os.path.exists("soulskill_autosave.json"):
            try:
                with open("soulskill_autosave.json", "r", encoding='utf-8') as f:
                    saved_data = json.load(f)
                    last_saved = saved_data.get('last_saved', '')
                    if last_saved:
                        saved_time = datetime.fromisoformat(last_saved)
                        time_diff = datetime.now() - saved_time
                        if time_diff.seconds < 60:
                            st.caption("💾 Auto-saved just now")
                        elif time_diff.seconds < 3600:
                            mins = time_diff.seconds // 60
                            st.caption(f"💾 Auto-saved {mins} min ago")
                        else:
                            st.caption(f"💾 Auto-saved {saved_time.strftime('%I:%M %p')}")
            except:
                pass
        
        st.markdown("### 📍 Quick Navigation")
        steps = ["Template", "Profile Type", "Personal Info", "AI Summary", "Skills", 
                 "Experience", "Work History", "Projects", "Education", "Preview", "ATS Check"]
        for i, step_name in enumerate(steps, 1):
            if i < st.session_state.step:
                if st.button(f"✅ {step_name}", key=f"nav_{i}", use_container_width=True):
                    goto_step(i)
            elif i == st.session_state.step:
                st.markdown(f"**▶️ {step_name}**")
            else:
                st.markdown(f"⚪ {step_name}")
    
    st.markdown("---")
    
    # Motivational message rotator
    import random
    motivational_messages = [
        "💪 Your dream job is just one great resume away!",
        "🌟 Every expert was once a beginner.",
        "🚀 Success is the sum of small efforts repeated.",
        "✨ Your future is created by what you do today.",
        "🎯 Believe in yourself and you're halfway there.",
        "💡 The only way to do great work is to love what you do.",
        "🏆 Your career breakthrough starts here!",
        "🌈 Turn your dreams into plans, plans into action."
    ]
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;
                text-align: center; font-size: 0.85rem; font-weight: 600;'>
        {random.choice(motivational_messages)}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Motivational message rotator
    import random
    motivational_messages = [
        "💪 Your dream job is just one great resume away!",
        "🌟 Every expert was once a beginner.",
        "🚀 Success is the sum of small efforts repeated.",
        "✨ Your future is created by what you do today.",
        "🎯 Believe in yourself and you're halfway there.",
        "💡 The only way to do great work is to love what you do.",
        "🏆 Your career breakthrough starts here!",
        "🌈 Turn your dreams into plans, plans into action."
    ]
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;
                text-align: center; font-size: 0.85rem; font-weight: 600;'>
        {random.choice(motivational_messages)}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("🌍 Global Standard")
    st.caption("🤖 AI-Powered")
    st.caption("📊 ATS-Optimized")
    st.caption("💎 Premium Quality")
    
    st.markdown("---")
    
    # Quick Links Section
    st.markdown("### 🔗 Career Resources")
    
    # Job Search Sites
    st.markdown("**💼 Job Boards:**")
    job_sites = [
        ("LinkedIn", "https://www.linkedin.com/jobs/"),
        ("Indeed", "https://www.indeed.com/"),
        ("Glassdoor", "https://www.glassdoor.com/"),
        ("Monster", "https://www.monster.com/"),
        ("Naukri", "https://www.naukri.com/"),
        ("AngelList", "https://www.angellist.com/jobs"),
    ]
    for name, url in job_sites:
        st.markdown(f"[{name}]({url})")
    
    st.markdown("---")
    
    # Learning Platforms
    st.markdown("**📚 Learning Platforms:**")
    learning_sites = [
        ("Coursera", "https://www.coursera.org/"),
        ("Udemy", "https://www.udemy.com/"),
        ("edX", "https://www.edx.org/"),
        ("LinkedIn Learning", "https://www.linkedin.com/learning/"),
        ("Pluralsight", "https://www.pluralsight.com/"),
        ("freeCodeCamp", "https://www.freecodecamp.org/"),
    ]
    for name, url in learning_sites:
        st.markdown(f"[{name}]({url})")
    
    st.markdown("---")
    
    # Interview Prep
    st.markdown("**🎯 Interview Prep:**")
    interview_sites = [
        ("LeetCode", "https://leetcode.com/"),
        ("HackerRank", "https://www.hackerrank.com/"),
        ("Pramp", "https://www.pramp.com/"),
        ("InterviewBit", "https://www.interviewbit.com/"),
    ]
    for name, url in interview_sites:
        st.markdown(f"[{name}]({url})")
    
    st.markdown("---")
    
    # Company Research
    st.markdown("**🏢 Company Research:**")
    research_sites = [
        ("Glassdoor Reviews", "https://www.glassdoor.com/Reviews/"),
        ("Crunchbase", "https://www.crunchbase.com/"),
        ("Built In", "https://builtin.com/"),
    ]
    for name, url in research_sites:
        st.markdown(f"[{name}]({url})")

# MAIN CONTENT

if st.session_state.step == 0:
    # Welcome Screen with Banner
    st.markdown("""
    <div class='welcome-banner'>
        <h1 style='font-size: 3.5rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>✨ SOULVEST</h1>
        <p style='font-size: 1.8rem; margin: 1rem 0 0.5rem 0; font-weight: 600;'>Enterprise AI Resume Builder</p>
        <p style='font-size: 1.2rem; margin: 0; opacity: 0.95;'>Where Career Dreams Become Reality</p>
    </div>
    """, unsafe_allow_html=True)
    
    # PWA Install Button
    st.markdown("""
    <div style='text-align: center; margin: 1.5rem 0;'>
        <button id='pwa-install-btn' style='display: none; 
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
            color: white; padding: 1rem 2rem; border: none; border-radius: 10px;
            font-size: 1.1rem; font-weight: 600; cursor: pointer;
            box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
            transition: all 0.3s ease;'>
            📱 Install Soulvest as App
        </button>
    </div>
    <style>
        #pwa-install-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(17, 153, 142, 0.6);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Success Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='stat-box'>
            <h2 style='color: #667eea; margin: 0;'>95%+</h2>
            <p style='margin: 0.5rem 0 0 0; color: #666;'>ATS Success</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-box'>
            <h2 style='color: #667eea; margin: 0;'>20+</h2>
            <p style='margin: 0.5rem 0 0 0; color: #666;'>Templates</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='stat-box'>
            <h2 style='color: #667eea; margin: 0;'>6</h2>
            <p style='margin: 0.5rem 0 0 0; color: #666;'>AI Features</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='stat-box'>
            <h2 style='color: #667eea; margin: 0;'>5</h2>
            <p style='margin: 0.5rem 0 0 0; color: #666;'>Export Formats</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Rotating Motivational Quotes
    career_quotes = [
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work.", "Steve Jobs"),
        ("Opportunities don't happen. You create them.", "Chris Grosser"),
        ("Don't be afraid to give up the good to go for the great.", "John D. Rockefeller"),
        ("The future depends on what you do today.", "Mahatma Gandhi"),
        ("Success usually comes to those who are too busy to be looking for it.", "Henry David Thoreau"),
        ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
        ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
        ("The secret of getting ahead is getting started.", "Mark Twain"),
        ("It's not whether you get knocked down, it's whether you get up.", "Vince Lombardi"),
        ("Choose a job you love, and you will never have to work a day in your life.", "Confucius"),
        ("I find that the harder I work, the more luck I seem to have.", "Thomas Jefferson"),
        ("Success is walking from failure to failure with no loss of enthusiasm.", "Winston Churchill"),
        ("What we fear doing most is usually what we most need to do.", "Tim Ferriss")
    ]
    
    selected_quote = random.choice(career_quotes)
    st.markdown(f"""
    <div class='motivational-quote'>
        "{selected_quote[0]}"<br>
        <small style='opacity: 0.8;'>— {selected_quote[1]}</small>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h2 style='color: #667eea;'>🤖 Advanced AI</h2>
            <p>• AI-generated summaries<br>
            • Cover letter generation<br>
            • Career advice engine<br>
            • Job matching analysis<br>
            • LinkedIn optimization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h2 style='color: #667eea;'>📊 Enterprise ATS</h2>
            <p>• 95%+ ATS compatibility<br>
            • Keyword optimization<br>
            • Competitive benchmarking<br>
            • Real-time scoring<br>
            • Format validation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h2 style='color: #667eea;'>💎 Premium Templates</h2>
            <p>• 20+ Professional designs<br>
            • Industry-specific layouts<br>
            • Multi-format export<br>
            • Mobile-friendly<br>
            • Global standards</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Another rotating quote for variety
    success_quotes = [
        ("The only impossible journey is the one you never begin.", "Tony Robbins"),
        ("Your limitation—it's only your imagination.", "Unknown"),
        ("Great things never come from comfort zones.", "Unknown"),
        ("Dream it. Wish it. Do it.", "Unknown"),
        ("Success doesn't just find you. You have to go out and get it.", "Unknown"),
        ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
        ("Dream bigger. Do bigger.", "Unknown"),
        ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
        ("Wake up with determination. Go to bed with satisfaction.", "Unknown"),
        ("Do something today that your future self will thank you for.", "Sean Patrick Flanery"),
        ("Little things make big days.", "Unknown"),
        ("It's going to be hard, but hard does not mean impossible.", "Unknown"),
        ("Don't wait for opportunity. Create it.", "Unknown"),
        ("Sometimes we're tested not to show our weaknesses, but to discover our strengths.", "Unknown"),
        ("The key to success is to focus on goals, not obstacles.", "Unknown")
    ]
    
    selected_quote2 = random.choice(success_quotes)
    st.markdown(f"""
    <div class='motivational-quote'>
        "{selected_quote2[0]}"<br>
        <small style='opacity: 0.8;'>— {selected_quote2[1]}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("### 🎯 Why Choose Soulvest?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **✨ AI-Powered Features:**
        - Professional summary generation
        - Cover letter writing
        - Career roadmap & advice
        - Interview preparation
        - LinkedIn profile optimization
        
        **📊 Smart Analytics:**
        - Comprehensive resume scoring (0-100)
        - Keyword density analysis
        - Competitive benchmarking
        - Industry-specific feedback
        - Real-time ATS compatibility
        """)
    
    with col2:
        st.markdown("""
        **💼 Export Options:**
        - PDF (ATS-optimized & design)
        - DOCX (editable format)
        - Plain Text (maximum ATS compatibility)
        - JSON (data portability)
        - Markdown (GitHub-ready)
        
        **🌍 Global Support:**
        - International resume formats
        - 25+ Industry-specific templates
        - Freshers & experienced professionals
        - Entry-level to C-suite
        - Open source & self-hosted
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Advanced Tools Section
    st.markdown("### 🛠️ Advanced Career Tools")
    tool_tabs = st.tabs(["📤 Import Resume", "📧 Email Templates", "📊 Keyword Analyzer", "📝 Length Optimizer", "📷 QR Code"])
    
    with tool_tabs[0]:
        st.markdown("#### 📤 Import Your Existing Resume")
        st.info("💡 Already have a resume? Upload it and we'll help you improve it!")
        
        uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, or TXT)", type=['pdf', 'docx', 'txt'])
        if uploaded_file:
            try:
                # Read file content
                content = uploaded_file.read()
                if uploaded_file.type == "text/plain":
                    text = content.decode('utf-8')
                else:
                    text = content.decode('utf-8', errors='ignore')
                
                # Parse resume
                parsed = ResumeImporter.parse_text_resume(text)
                
                if parsed['parsed_successfully']:
                    st.success("✅ Resume imported successfully!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if parsed.get('full_name'):
                            st.info(f"📝 Name: {parsed['full_name']}")
                        if parsed.get('email'):
                            st.info(f"📧 Email: {parsed['email']}")
                    with col2:
                        if parsed.get('phone'):
                            st.info(f"📞 Phone: {parsed['phone']}")
                    
                    # Suggest improvements
                    suggestions = ResumeImporter.suggest_improvements(parsed)
                    if suggestions:
                        st.markdown("**🎯 Suggested Improvements:**")
                        for suggestion in suggestions:
                            st.warning(suggestion)
                    
                    if st.button("✨ Optimize This Resume with AI"):
                        # Pre-fill session state with parsed data
                        if parsed.get('full_name'):
                            st.session_state.full_name = parsed['full_name']
                        if parsed.get('email'):
                            st.session_state.email = parsed['email']
                        if parsed.get('phone'):
                            st.session_state.phone = parsed['phone']
                        next_step()
                        st.rerun()
                else:
                    st.error("⚠️ Could not parse resume. Please try a different format or build from scratch.")
            except Exception as e:
                st.error(f"⚠️ Error reading file: {str(e)}")
    
    with tool_tabs[1]:
        st.markdown("#### 📧 Professional Email Templates")
        st.info("💡 Stand out with professionally crafted emails for every job search stage!")
        
        templates = EmailTemplates.get_all_templates()
        template_options = {t['name']: t['type'] for t in templates}
        
        selected_template = st.selectbox(
            "Choose email type",
            options=list(template_options.keys()),
            help="Select the type of professional email you need"
        )
        
        template_type = template_options[selected_template]
        template = EmailTemplates.get_template(template_type)
        
        st.markdown(f"**📋 Template: {template['name']}**")
        
        # Input fields for template
        col1, col2 = st.columns(2)
        with col1:
            your_name = st.text_input("Your Name", value=st.session_state.get('full_name', ''))
            position = st.text_input("Position Title", value="Software Engineer")
            company = st.text_input("Company Name", value="TechCorp")
        with col2:
            your_email = st.text_input("Your Email", value=st.session_state.get('email', ''))
            your_phone = st.text_input("Your Phone", value=st.session_state.get('phone', ''))
            years = st.text_input("Years of Experience", value="3")
        
        # Generate email
        if st.button("✉️ Generate Email", key="gen_email"):
            data = {
                "your_name": your_name,
                "position": position,
                "company": company,
                "email": your_email,
                "phone": your_phone,
                "years": years,
                "field": st.session_state.get('industry', 'your field'),
                "key_achievement": "my proven track record in delivering results",
                "interviewer_name": "Hiring Manager",
                "specific_topic_discussed": "the innovative projects",
                "relevant_skill": st.session_state.get('tech_skills', 'technical skills')
            }
            
            filled = EmailTemplates.fill_template(template_type, data)
            
            st.markdown("---")
            st.markdown("**📤 Subject:**")
            st.code(filled['subject'])
            st.markdown("**📝 Email Body:**")
            st.text_area("", value=filled['body'], height=300, label_visibility="collapsed")
            st.success("✅ Email generated! Copy and personalize before sending.")
    
    with tool_tabs[2]:
        st.markdown("#### 📊 Real-Time Keyword Analyzer")
        st.info("💡 See which keywords match the job description instantly!")
        
        col1, col2 = st.columns(2)
        with col1:
            sample_resume = st.text_area(
                "Your Resume Text",
                placeholder="Paste your resume content here...",
                height=200,
                help="Paste your resume text to analyze"
            )
        with col2:
            job_desc_sample = st.text_area(
                "Job Description",
                placeholder="Paste the job description here...",
                height=200,
                help="Paste the job posting you're targeting"
            )
        
        if st.button("🔍 Analyze Keywords", key="analyze_kw"):
            if sample_resume and job_desc_sample:
                result = KeywordHighlighter.highlight_keywords(sample_resume, job_desc_sample)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Keyword Density", f"{result['keyword_density']}%")
                with col2:
                    st.metric("Matched Keywords", f"{result['matched_count']}/{result['total_jd_keywords']}")
                with col3:
                    status_color = "🟢" if result['status'] == "Excellent" else "🟡" if result['status'] == "Good" else "🔴"
                    st.metric("Status", f"{status_color} {result['status']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Matched Keywords:**")
                    for kw in result['matched_keywords'][:15]:
                        st.success(f"✓ {kw}")
                with col2:
                    st.markdown("**❌ Missing Keywords (Top 15):**")
                    for kw in result['missing_keywords'][:15]:
                        st.error(f"✗ {kw}")
                
                if result['keyword_density'] < 50:
                    st.warning("⚠️ Your keyword density is low. Consider adding more relevant keywords from the job description.")
                else:
                    st.success("🎯 Good keyword coverage! Your resume aligns well with the job requirements.")
            else:
                st.error("Please provide both resume text and job description.")
    
    with tool_tabs[3]:
        st.markdown("#### 📝 Resume Length Optimizer")
        st.info("💡 Get the perfect resume length for your experience level!")
        
        target_pages = st.slider("Target Resume Pages", 1, 3, 1, help="1 page for <5 years exp, 2 pages for 5-15 years, 3 pages for 15+ years")
        
        if st.button("📏 Analyze Current Resume", key="analyze_length"):
            analysis = ResumeLengthOptimizer.analyze_length(st.session_state, target_pages)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Words", analysis['total_words'])
            with col2:
                st.metric("Target Words", analysis['target_words'])
            with col3:
                st.metric("Estimated Pages", analysis['estimated_pages'])
            
            status_color = "🟢" if analysis['status'] == "Perfect Length" else "🟡" if analysis['status'] == "Too Short" else "🔴"
            st.markdown(f"### {status_color} Status: {analysis['status']}")
            
            if analysis['recommendations']:
                st.markdown("**💡 Recommendations:**")
                for rec in analysis['recommendations']:
                    st.info(rec)
            
            if analysis.get('sections'):
                st.markdown("**📊 Section Breakdown:**")
                for section in analysis['sections']:
                    essential = "🔴 Essential" if section['essential'] else "🟡 Optional"
                    st.caption(f"{section['name']}: {section['words']} words {essential}")
    
    with tool_tabs[4]:
        st.markdown("#### 📷 QR Code Generator")
        st.info("💡 Add a QR code to your resume for easy contact sharing!")
        
        st.markdown("Your resume will include a QR code with your contact information:")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.session_state.get('full_name'):
                st.text_input("Name", value=st.session_state.get('full_name', ''), disabled=True)
                st.text_input("Email", value=st.session_state.get('email', ''), disabled=True)
                st.text_input("Phone", value=st.session_state.get('phone', ''), disabled=True)
                st.text_input("LinkedIn", value=st.session_state.get('linkedin', ''), disabled=True)
                
                if st.button("🎨 Generate QR Code"):
                    vcard_data = QRCodeGenerator.generate_contact_qr_data(st.session_state)
                    qr_url = QRCodeGenerator.get_qr_code_url(vcard_data)
                    
                    with col2:
                        st.markdown("**📱 Your QR Code:**")
                        st.image(qr_url, width=200)
                        st.success("✅ Add this to your resume!")
                        st.caption("Recruiters can scan this to save your contact instantly!")
            else:
                st.warning("⚠️ Complete your personal information first to generate a QR code.")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 Start Building Your Resume", use_container_width=True):
            next_step()
    
    st.markdown("---")
    
    # Success Stories Carousel
    st.markdown("### 💼 Success Stories")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='success-story'>
            <p style='margin: 0; font-weight: 600;'>"Got 3 interviews in one week!"</p>
            <small style='opacity: 0.9;'>— Software Engineer, Landing Dream Job</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='success-story'>
            <p style='margin: 0; font-weight: 600;'>"ATS score went from 45 to 92!"</p>
            <small style='opacity: 0.9;'>— Marketing Manager, Career Transition</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("🎯 **Start Your Success Story**: Join thousands who transformed their careers with Soulvest. Our AI-powered platform creates resumes that pass ATS systems and impress recruiters!")

elif st.session_state.step == 1:
    # Template Selection - FIRST STEP like ResumeGemini
    st.title("🎨 Choose Your Resume Template")
    
    st.markdown("""
    <div class='motivational-quote'>
        "Start with a stunning template. Choose one now and customize it later! 🎨"
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Don't worry!** You can change your template anytime with one click.")
    
    all_templates = {**TEMPLATES, **INDIAN_TEMPLATES}
    
    # Template Gallery
    st.markdown("### 📱 Professional Templates")
    
    # Create tabs for different categories
    tab1, tab2 = st.tabs(["🌟 Modern Templates", "🇮🇳 India-Focused Templates"])
    
    with tab1:
        cols = st.columns(3)
        for idx, (template_name, template_config) in enumerate(TEMPLATES.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="border:2px solid {'#667eea' if st.session_state.get('template') == template_name else '#ddd'};
                            border-radius:12px;padding:15px;background:white;height:300px;
                            cursor:pointer;transition:all 0.3s;">
                    <h4 style="color:{template_config['color']};margin:0;">{template_name}</h4>
                    <p style="font-size:0.85rem;color:#666;margin:5px 0;">{template_config.get('description', 'Professional template')}</p>
                    <div style="background:#f8f9fa;padding:15px;border-radius:8px;margin:10px 0;font-size:0.75rem;">
                        <div style="color:{template_config['color']};font-weight:bold;margin-bottom:5px;">JOHN DOE</div>
                        <div style="color:#666;">Software Engineer</div>
                        <div style="border-top:2px solid {template_config['color']};margin:8px 0;"></div>
                        <div style="font-size:0.7rem;color:#999;">📧 email@example.com</div>
                    </div>
                    <small><strong>Font:</strong> {template_config['font']}<br>
                    <strong>Color:</strong> {template_config['color']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {template_name}", key=f"sel_{template_name}", use_container_width=True):
                    st.session_state.template = template_name
                    st.session_state.template_config = template_config
                    st.success(f"✅ {template_name} selected!")
                    st.rerun()
    
    with tab2:
        cols = st.columns(3)
        for idx, (template_name, template_config) in enumerate(INDIAN_TEMPLATES.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="border:2px solid {'#667eea' if st.session_state.get('template') == template_name else '#ddd'};
                            border-radius:12px;padding:15px;background:white;height:300px;">
                    <h4 style="color:{template_config['color']};margin:0;">{template_name}</h4>
                    <p style="font-size:0.85rem;color:#666;margin:5px 0;">{template_config.get('description', 'India-optimized template')}</p>
                    <div style="background:#f8f9fa;padding:15px;border-radius:8px;margin:10px 0;font-size:0.75rem;">
                        <div style="color:{template_config['color']};font-weight:bold;margin-bottom:5px;">PRIYA SHARMA</div>
                        <div style="color:#666;">Data Scientist</div>
                        <div style="border-top:2px solid {template_config['color']};margin:8px 0;"></div>
                        <div style="font-size:0.7rem;color:#999;">📧 email@example.com</div>
                    </div>
                    <small><strong>Font:</strong> {template_config['font']}<br>
                    <strong>Color:</strong> {template_config['color']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {template_name}", key=f"sel_{template_name}", use_container_width=True):
                    st.session_state.template = template_name
                    st.session_state.template_config = template_config
                    st.success(f"✅ {template_name} selected!")
                    st.rerun()
    
    st.markdown("---")
    
    if st.session_state.get('template'):
        st.success(f"✅ Selected Template: **{st.session_state.template}**")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("⬅️ Back"):
                prev_step()
        with col2:
            if st.button("Next: Choose Your Profile ➡️", use_container_width=True):
                next_step()
    else:
        st.warning("👆 Please select a template to continue")
        if st.button("⬅️ Back to Home"):
            prev_step()

elif st.session_state.step == 2:
    # Profile Type - moved from step 1
    st.title("👤 Choose Your Profile Type")
    
    st.markdown("""
    <div class='motivational-quote'>
        "Every career path is unique. Choose yours and let's make it shine! 🌟"
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎓 FRESHER\n\nRecent Graduate\nNo Work Experience\nLooking for First Job", use_container_width=True, help="For students and recent graduates"):
            st.session_state.profile_type = "fresher"
            next_step()
    
    with col2:
        if st.button("💼 EXPERIENCED\n\nWorking Professional\nHave Work Experience\nCareer Growth", use_container_width=True, help="For professionals with work experience"):
            st.session_state.profile_type = "experienced"
            next_step()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()

elif st.session_state.step == 3:
    # Personal Information - moved from step 2
    st.title("📝 Personal Information")
    
    # Profile Photo Upload Section
    st.markdown("### 📸 Profile Photo (Optional)")
    col_photo, col_preview = st.columns([2, 1])
    with col_photo:
        st.info("💡 Adding a professional photo makes your resume more personal and memorable!")
        photo = st.file_uploader("Upload your professional photo", type=["jpg", "jpeg", "png"], help="Recommended: Professional headshot with neutral background")
        if photo:
            encoded = base64.b64encode(photo.read()).decode()
            st.session_state.profile_photo_base64 = encoded
            st.success("✅ Photo uploaded successfully!")
    with col_preview:
        if st.session_state.get('profile_photo_base64'):
            st.markdown("**Preview:**")
            st.markdown(f'<img src="data:image/png;base64,{st.session_state.profile_photo_base64}" style="width:150px;height:150px;border-radius:50%;object-fit:cover;border:3px solid #667eea;">', unsafe_allow_html=True)
        else:
            st.caption("📷 Photo preview will appear here")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.full_name = st.text_input("Full Name *", value=st.session_state.get("full_name", ""))
        st.session_state.email = st.text_input("Email Address *", value=st.session_state.get("email", ""))
        st.session_state.phone = st.text_input("Phone Number *", value=st.session_state.get("phone", ""), placeholder="+91-XXXXX-XXXXX")
    
    with col2:
        city_list = ["Select City"] + MAJOR_INDIAN_CITIES
        city_idx = 0
        if "city" in st.session_state and st.session_state.city in MAJOR_INDIAN_CITIES:
            city_idx = MAJOR_INDIAN_CITIES.index(st.session_state.city) + 1
        st.session_state.city = st.selectbox("City *", city_list, index=city_idx)
        
        state_list = ["Select State"] + INDIAN_STATES
        state_idx = 0
        if "state" in st.session_state and st.session_state.state in INDIAN_STATES:
            state_idx = INDIAN_STATES.index(st.session_state.state) + 1
        st.session_state.state = st.selectbox("State *", state_list, index=state_idx)
        
        st.session_state.linkedin = st.text_input("LinkedIn Profile", value=st.session_state.get("linkedin", ""), placeholder="https://linkedin.com/in/yourprofile")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        ind_list = ["Select Industry"] + INDUSTRY_OPTIONS
        ind_idx = 0
        if "industry" in st.session_state and st.session_state.industry in INDUSTRY_OPTIONS:
            ind_idx = INDUSTRY_OPTIONS.index(st.session_state.industry) + 1
        st.session_state.industry = st.selectbox("Target Industry *", ind_list, index=ind_idx)
    with col2:
        st.session_state.job_title_target = st.text_input("Target Job Title *", value=st.session_state.get("job_title_target", ""), placeholder="e.g., Software Developer")
    
    # Languages
    st.markdown("### 🗣️ Languages Known")
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        lang_name = st.text_input("Language", key="lang", placeholder="e.g., English, Hindi")
    with col2:
        lang_prof = st.selectbox("Proficiency", ["Native", "Fluent", "Professional", "Basic"])
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add"):
            if lang_name:
                st.session_state.language_entries.append({"language": lang_name, "proficiency": lang_prof})
                st.rerun()
    
    if st.session_state.language_entries:
        for idx, lang in enumerate(st.session_state.language_entries):
            col1, col2 = st.columns([4,1])
            with col1:
                st.write(f"• {lang['language']} - {lang['proficiency']}")
            with col2:
                if st.button("❌", key=f"del_lang_{idx}"):
                    st.session_state.language_entries.pop(idx)
                    st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            if all([st.session_state.get("full_name"), st.session_state.get("email"), 
                   st.session_state.get("phone"), st.session_state.city != "Select City"]):
                next_step()
            else:
                st.error("Please fill all required fields (*)")

elif st.session_state.step == 4:
    # AI-Powered Professional Summary
    st.title("🤖 Professional Summary (AI-Powered)")
    
    # Show pre-written examples based on job title
    job_title = st.session_state.get('job_title_target', '')
    if job_title:
        examples = get_examples_for_role(job_title)
        if examples['summaries']:
            with st.expander("💡 Click to use pre-written examples", expanded=True):
                st.markdown("**Choose a professional summary to start with:**")
                for idx, summary_example in enumerate(examples['summaries']):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"<small>{summary_example}</small>", unsafe_allow_html=True)
                    with col2:
                        if st.button("Use This", key=f"summary_{idx}"):
                            st.session_state.summary = summary_example
                            st.success("✅ Example added! You can edit it below.")
                            st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.ai_enabled:
            st.markdown("""
            <div class='tip-box'>
                <strong>🤖 AI Assistant Ready!</strong><br>
                Click "Generate with AI" to create a professional summary tailored to your profile.
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✨ Generate Summary with AI", use_container_width=True):
                with st.spinner("AI is writing your summary..."):
                    profile_data = {
                        'profile_type': st.session_state.profile_type,
                        'full_name': st.session_state.get('full_name', ''),
                        'job_title_target': st.session_state.get('job_title_target', ''),
                        'industry': st.session_state.get('industry', ''),
                        'tech_skills': st.session_state.get('tech_skills', ''),
                        'soft_skills': st.session_state.get('soft_skills', '')
                    }
                    summary = ai_assistant.generate_professional_summary(profile_data)
                    st.session_state.summary = summary
                    st.success("✅ AI has generated your summary!")
                    st.rerun()
        else:
            st.warning("⚠️ AI features are disabled. Add your Google Gemini API key to enable AI generation.")
        
        st.session_state.summary = st.text_area(
            "Your Professional Summary",
            value=st.session_state.get("summary", ""),
            height=200,
            help="3-5 sentences highlighting your strengths and career goals"
        )
        
        # Spell and grammar check
        if st.session_state.get("summary"):
            if st.button("🔍 Check Spelling & Style", key="check_summary"):
                issues = SpellChecker.check_text(st.session_state.summary)
                if issues:
                    st.markdown("**📝 Suggestions:**")
                    for issue in issues:
                        if issue['type'] == 'spelling':
                            st.warning(f"Spelling: {issue['message']}")
                        else:
                            st.info(f"Style: {issue['message']} → {issue['suggestion']}")
                else:
                    st.success("✅ No issues found! Your text looks great.")
    
    with col2:
        st.markdown("### 💡 Writing Tips")
        st.markdown("""
        **Include:**
        - Your experience level
        - Key skills
        - Career goals
        - Unique value
        
        **ATS Keywords:**
        """)
        if st.session_state.get('industry') and st.session_state.industry in INDUSTRY_KEYWORDS:
            keywords = INDUSTRY_KEYWORDS[st.session_state.industry][:5]
            for kw in keywords:
                st.caption(f"✓ {kw}")
    
    # Sample summaries
    with st.expander("📝 View Sample Summaries"):
        if st.session_state.profile_type == "fresher":
            st.markdown("""
            **Sample for Fresher:**
            
            *Recent Computer Science graduate with strong foundation in Python, Java, and web development. 
            Completed multiple academic projects demonstrating problem-solving and teamwork skills. 
            Eager to contribute technical skills and fresh perspective to a dynamic software development team.*
            """)
        else:
            st.markdown("""
            **Sample for Experienced:**
            
            *Results-driven Software Engineer with 5+ years of experience in full-stack development. 
            Proven track record of delivering scalable applications using React, Node.js, and AWS. 
            Strong expertise in agile methodologies and cross-functional collaboration. 
            Seeking to leverage technical leadership skills to drive innovation.*
            """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            if st.session_state.get("summary", "").strip():
                next_step()
            else:
                st.error("Please write your professional summary")

elif st.session_state.step == 5:
    # Skills with AI Suggestions
    st.title("🧠 Skills & Competencies")
    
    # Show pre-written skill suggestions
    job_title = st.session_state.get('job_title_target', '')
    if job_title:
        with st.expander("💡 Click to add popular skills", expanded=True):
            st.markdown("**Click to add skills to your resume:**")
            
            # Show skills from SKILLS_EXAMPLES
            cols = st.columns(3)
            skill_categories = list(SKILLS_EXAMPLES.keys())[:6]  # Show 6 categories
            for idx, category in enumerate(skill_categories):
                with cols[idx % 3]:
                    st.markdown(f"**{category}:**")
                    for skill in SKILLS_EXAMPLES[category][:5]:  # Top 5 from each
                        if st.button(f"+ {skill}", key=f"skill_{skill}_{idx}"):
                            current_skills = st.session_state.get('tech_skills', '')
                            if current_skills:
                                st.session_state.tech_skills = current_skills + ", " + skill
                            else:
                                st.session_state.tech_skills = skill
                            st.success(f"✅ Added {skill}!")
                            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Technical Skills")
        st.session_state.tech_skills = st.text_area(
            "Enter technical skills (comma-separated)",
            value=st.session_state.get("tech_skills", ""),
            height=150,
            placeholder="Python, Java, SQL, AWS, React"
        )
        
        if st.session_state.ai_enabled:
            if st.button("🤖 AI Suggest Technical Skills"):
                with st.spinner("AI is analyzing your profile..."):
                    suggestions = ai_assistant.suggest_skills(
                        st.session_state.get('job_title_target', ''),
                        st.session_state.get('industry', ''),
                        st.session_state.get('tech_skills', '')
                    )
                    if suggestions:
                        st.success("✅ AI Suggestions:")
                        st.write(", ".join(suggestions))
    
    with col2:
        st.markdown("### Soft Skills")
        st.session_state.soft_skills = st.text_area(
            "Enter soft skills (comma-separated)",
            value=st.session_state.get("soft_skills", ""),
            height=150,
            placeholder="Communication, Leadership, Problem Solving"
        )
    
    # Industry-specific suggestions
    if st.session_state.get('industry') and st.session_state.industry in INDUSTRY_KEYWORDS:
        st.markdown("### 💡 Recommended Skills for " + st.session_state.industry)
        keywords = INDUSTRY_KEYWORDS[st.session_state.industry]
        cols = st.columns(4)
        for idx, kw in enumerate(keywords[:12]):
            with cols[idx % 4]:
                st.caption(f"✓ {kw}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            next_step()

elif st.session_state.step == 6:
    # Experience Overview
    st.title("💼 Experience Overview")
    
    if st.session_state.profile_type == "fresher":
        st.markdown("### Internships / Training / Academic Projects")
        st.caption("Add any relevant experience including internships, industrial training, or significant projects")
    else:
        st.markdown("### Professional Experience Summary")
    
    st.session_state.experience = st.text_area(
        "Brief Overview",
        value=st.session_state.get("experience", ""),
        height=120,
        help="2-3 sentences summarizing your overall experience"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            next_step()

elif st.session_state.step == 7:
    # Work History with AI Enhancement
    st.title("📜 Work History / Experience Details")
    
    # Show pre-written examples
    job_title = st.session_state.get('job_title_target', '')
    if job_title:
        examples = get_examples_for_role(job_title)
        if examples['bullets']:
            with st.expander("💡 Click to use pre-written bullet points"):
                st.markdown("**Choose responsibilities to add to your job description:**")
                for idx, bullet_example in enumerate(examples['bullets'][:5]):  # Show top 5
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"<small>• {bullet_example}</small>", unsafe_allow_html=True)
                    with col2:
                        if st.button("Add", key=f"bullet_{idx}"):
                            current_resp = st.session_state.get('resp_input_text', '')
                            new_resp = current_resp + "\n• " + bullet_example if current_resp else "• " + bullet_example
                            st.session_state.resp_input_text = new_resp
                            st.success("✅ Added!")
                            st.rerun()
    
    st.markdown("### Add Work Experience")
    
    col1, col2 = st.columns(2)
    with col1:
        job_title_input = st.text_input("Job Title / Role *", key="job_title_input")
        company_name = st.text_input("Company Name *", key="company_input")
    with col2:
        duration = st.text_input("Duration *", key="duration_input", placeholder="Jan 2022 - Present")
        location = st.text_input("Location", key="location_input", placeholder="Mumbai, Maharashtra")
    
    responsibilities = st.text_area(
        "Responsibilities & Achievements *",
        value=st.session_state.get('resp_input_text', ''),
        key="resp_input",
        height=150,
        help="Describe your key responsibilities and achievements"
    )
    # Store the text area value
    st.session_state.resp_input_text = responsibilities
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add Work Entry"):
            if job_title_input and company_name and duration and responsibilities:
                st.session_state.work_entries.append({
                    'title': job_title_input,
                    'company': company_name,
                    'duration': duration,
                    'location': location,
                    'responsibilities': responsibilities
                })
                st.session_state.resp_input_text = ''  # Clear after adding
                st.success("✅ Work entry added!")
                st.rerun()
            else:
                st.error("Please fill all required fields")
    
    with col2:
        if st.session_state.ai_enabled and job_title_input and company_name and responsibilities:
            if st.button("🤖 Enhance with AI"):
                with st.spinner("AI is enhancing your description..."):
                    enhanced = ai_assistant.enhance_work_description(job_title, company_name, responsibilities)
                    st.success("✅ AI Enhanced Version:")
                    st.text_area("Copy this enhanced version:", enhanced, height=150)
    
    # Display added entries
    if st.session_state.work_entries:
        st.markdown("---")
        st.markdown("### 📋 Added Work Experiences")
        for idx, work in enumerate(st.session_state.work_entries):
            with st.expander(f"{work['title']} at {work['company']}"):
                st.write(f"**Duration:** {work['duration']}")
                if work.get('location'):
                    st.write(f"**Location:** {work['location']}")
                st.write(f"**Responsibilities:**\n{work['responsibilities']}")
                if st.button("🗑️ Remove", key=f"del_work_{idx}"):
                    st.session_state.work_entries.pop(idx)
                    st.rerun()
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            next_step()

elif st.session_state.step == 8:
    # Projects
    st.title("🚀 Projects")
    
    col1, col2 = st.columns(2)
    with col1:
        proj_name = st.text_input("Project Name *", key="proj_name")
        proj_duration = st.text_input("Duration", key="proj_dur", placeholder="Jan 2023 - Mar 2023")
    with col2:
        proj_tech = st.text_input("Technologies Used", key="proj_tech", placeholder="Python, Django, PostgreSQL")
    
    proj_desc = st.text_area("Project Description *", key="proj_desc", height=120)
    
    if st.button("➕ Add Project"):
        if proj_name and proj_desc:
            st.session_state.project_entries.append({
                'name': proj_name,
                'duration': proj_duration,
                'technologies': proj_tech,
                'description': proj_desc
            })
            st.success("✅ Project added!")
            st.rerun()
    
    if st.session_state.project_entries:
        st.markdown("### 📋 Added Projects")
        for idx, proj in enumerate(st.session_state.project_entries):
            with st.expander(f"{proj['name']}"):
                st.write(f"**Technologies:** {proj.get('technologies', 'N/A')}")
                st.write(f"**Description:** {proj['description']}")
                if st.button("🗑️ Remove", key=f"del_proj_{idx}"):
                    st.session_state.project_entries.pop(idx)
                    st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            next_step()

elif st.session_state.step == 9:
    # Education
    st.title("🎓 Education")
    
    col1, col2 = st.columns(2)
    with col1:
        edu_degree = st.selectbox("Degree *", DEGREE_OPTIONS, key="edu_deg")
        edu_stream = st.selectbox("Stream/Specialization *", STREAM_OPTIONS, key="edu_stream")
    with col2:
        edu_inst = st.text_input("Institution Name *", key="edu_inst")
        edu_univ = st.text_input("University/Board", key="edu_univ")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        edu_year = st.text_input("Year of Completion *", key="edu_year", placeholder="2024")
    with col2:
        edu_grade = st.text_input("Grade/Percentage", key="edu_grade", placeholder="8.5 CGPA / 85%")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Education"):
            if edu_degree and edu_stream and edu_inst and edu_year:
                st.session_state.education_entries.append({
                    'degree': edu_degree,
                    'stream': edu_stream,
                    'institution': edu_inst,
                    'university': edu_univ,
                    'year': edu_year,
                    'grade': edu_grade
                })
                st.success("✅ Education added!")
                st.rerun()
    
    if st.session_state.education_entries:
        st.markdown("### 📋 Added Education")
        for idx, edu in enumerate(st.session_state.education_entries):
            with st.expander(f"{edu['degree']} in {edu['stream']}"):
                st.write(f"**Institution:** {edu['institution']}")
                st.write(f"**Year:** {edu['year']} | **Grade:** {edu.get('grade', 'N/A')}")
                if st.button("🗑️ Remove", key=f"del_edu_{idx}"):
                    st.session_state.education_entries.pop(idx)
                    st.rerun()
    
    # Certifications
    st.markdown("---")
    st.markdown("### 🏆 Certifications (Optional)")
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        cert_name = st.text_input("Certification Name", key="cert_name")
    with col2:
        cert_issuer = st.text_input("Issuing Organization", key="cert_issuer")
    with col3:
        cert_year = st.text_input("Year", key="cert_year")
    
    if st.button("➕ Add Certification"):
        if cert_name:
            st.session_state.certification_entries.append({
                'name': cert_name,
                'issuer': cert_issuer,
                'year': cert_year
            })
            st.success("✅ Certification added!")
            st.rerun()
    
    if st.session_state.certification_entries:
        for idx, cert in enumerate(st.session_state.certification_entries):
            col1, col2 = st.columns([4,1])
            with col1:
                st.write(f"• {cert['name']} - {cert.get('issuer', '')} ({cert.get('year', '')})")
            with col2:
                if st.button("❌", key=f"del_cert_{idx}"):
                    st.session_state.certification_entries.pop(idx)
                    st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️"):
            if st.session_state.education_entries:
                next_step()
            else:
                st.error("Please add at least one education entry")

elif st.session_state.step == 10:
    # Preview and Download
    st.title("📄 Resume Preview & Customization")
    
    # Template customization section
    st.markdown("### 🎨 Customize Your Resume")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        all_templates = {**TEMPLATES, **INDIAN_TEMPLATES}
        current_template = st.session_state.get('template', list(all_templates.keys())[0])
        new_template = st.selectbox(
            "Change Template",
            list(all_templates.keys()),
            index=list(all_templates.keys()).index(current_template) if current_template in all_templates else 0
        )
        if new_template != current_template:
            st.session_state.template = new_template
            st.success(f"✅ Switched to {new_template}!")
            st.rerun()
    
    with col2:
        template_config = all_templates[st.session_state.template]
        # Color customization
        colors = {
            "Professional Blue": "#2c3e50",
            "Success Green": "#27ae60",
            "Corporate Purple": "#8e44ad",
            "Modern Teal": "#16a085",
            "Classic Navy": "#34495e",
            "Elegant Maroon": "#c0392b"
        }
        selected_color = st.selectbox("Accent Color", list(colors.keys()))
        if st.button("Apply Color"):
            template_config['color'] = colors[selected_color]
            st.session_state.template_config = template_config
            st.success("✅ Color updated!")
            st.rerun()
    
    with col3:
        # Font customization
        fonts = ["Arial", "Georgia", "Times New Roman", "Calibri", "Helvetica", "Verdana"]
        selected_font = st.selectbox("Font Style", fonts)
        if st.button("Apply Font"):
            template_config['font'] = selected_font
            st.session_state.template_config = template_config
            st.success("✅ Font updated!")
            st.rerun()
    
    st.markdown("---")
    
    # Profile photo section - enhanced
    if not st.session_state.get('profile_photo_base64'):
        st.markdown("### 📸 Add Your Photo (Optional)")
        col_photo, col_info = st.columns([2, 1])
        with col_photo:
            st.info("💡 Professional photo makes your resume stand out!")
            photo = st.file_uploader("Upload your professional photo", type=["jpg", "jpeg", "png"], key="photo_preview")
            if photo:
                encoded = base64.b64encode(photo.read()).decode()
                st.session_state.profile_photo_base64 = encoded
                st.success("✅ Photo added successfully!")
                st.rerun()
        with col_info:
            st.markdown("**Tips:**")
            st.caption("✓ Professional headshot")
            st.caption("✓ Neutral background")
            st.caption("✓ Good lighting")
            st.caption("✓ Business attire")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success("✅ Profile photo already added!")
        with col2:
            if st.button("🔄 Change Photo"):
                del st.session_state.profile_photo_base64
                st.rerun()
    
    st.markdown("---")
    
    # Additional links
    st.markdown("### 🔗 Additional Links")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.github = st.text_input("GitHub Profile", value=st.session_state.get("github", ""), placeholder="https://github.com/yourusername")
    with col2:
        st.session_state.portfolio = st.text_input("Portfolio Website", value=st.session_state.get("portfolio", ""), placeholder="https://yourportfolio.com")
    
    st.markdown("---")
    
    # Generate resume
    all_templates = {**TEMPLATES, **INDIAN_TEMPLATES}
    template_config = all_templates[st.session_state.template]
    
    try:
        resume_html = generate_resume_html(st.session_state, template_config)
    except UnicodeEncodeError as e:
        st.error("❌ Error generating resume. Please check your input for special characters.")
        st.error(f"Details: {str(e)}")
        resume_html = "<html><body><h1>Error generating resume</h1></body></html>"
    
    st.markdown("### 👀 Preview")
    try:
        st.components.v1.html(resume_html, height=800, scrolling=True)
    except Exception as e:
        st.error("Error displaying preview. The resume can still be downloaded.")
    
    # Download button
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Encode HTML properly to handle Unicode characters
        resume_html_bytes = resume_html.encode('utf-8', errors='ignore')
        st.download_button(
            "📥 Download HTML",
            resume_html_bytes,
            file_name=f"Resume_{st.session_state.get('full_name', 'Resume').replace(' ', '_')}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col2:
        if PDF_AVAILABLE:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    pdfkit.from_string(resume_html, tmp.name)
                    with open(tmp.name, "rb") as f:
                        pdf_data = f.read()
                    st.download_button(
                        "📥 Download PDF",
                        pdf_data,
                        file_name=f"Resume_{st.session_state.get('full_name', 'Resume').replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except:
                st.warning("PDF generation not available")
        else:
            st.info("Install pdfkit for PDF support")
    
    with col3:
        # Save progress & version control
        version_name = st.text_input("Version Name (optional)", value=f"Version {datetime.now().strftime('%m-%d %H:%M')}", key="version_name")
        if st.button("💾 Save Version", use_container_width=True):
            data = dict(st.session_state)
            
            # Initialize versions list if not exists
            if 'saved_versions' not in st.session_state:
                st.session_state.saved_versions = []
            
            # Create version
            version = ResumeVersionControl.save_version(data, version_name)
            st.session_state.saved_versions.append(version)
            
            # Also save to file
            with open("soulskill_progress.json", "w") as f:
                json.dump({k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, list, dict))}, f)
            
            st.success(f"✅ Version '{version['version_name']}' saved! (Completeness: {version['stats']['completeness']}%)")
    
    # Version history
    if st.session_state.get('saved_versions'):
        with st.expander(f"📚 Version History ({len(st.session_state.saved_versions)} versions)"):
            for idx, version in enumerate(reversed(st.session_state.saved_versions)):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**{version['version_name']}**")
                    st.caption(f"Created: {version['created_at']}")
                with col2:
                    st.metric("Completeness", f"{version['stats']['completeness']}%")
                with col3:
                    st.metric("Sections", version['stats']['sections'])
                st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            prev_step()
    with col2:
        if st.button("Next ➡️ ATS Check"):
            next_step()

elif st.session_state.step == 11:
    # ATS Optimization Check
    st.title("📊 ATS Compatibility Check")
    
    st.markdown("""
    <div class='tip-box'>
        <strong>💡 What is ATS?</strong><br>
        Applicant Tracking Systems (ATS) are used by 90% of companies to screen resumes. 
        This tool helps ensure your resume passes ATS screening!
    </div>
    """, unsafe_allow_html=True)
    
    # Job description input
    st.markdown("### 📋 Paste Job Description")
    st.caption("Paste the job description you're applying for to get a detailed ATS match score")
    
    job_desc = st.text_area(
        "Job Description",
        value=st.session_state.get("job_description", ""),
        height=200,
        placeholder="Paste the complete job description here..."
    )
    
    if st.button("🔍 Analyze ATS Compatibility", use_container_width=True):
        if job_desc:
            with st.spinner("Analyzing your resume..."):
                # Compile resume text
                resume_text = f"""
                {st.session_state.get('full_name', '')}
                {st.session_state.get('job_title_target', '')}
                {st.session_state.get('summary', '')}
                {st.session_state.get('tech_skills', '')}
                {st.session_state.get('soft_skills', '')}
                {st.session_state.get('experience', '')}
                """
                
                for work in st.session_state.work_entries:
                    resume_text += f" {work['title']} {work['company']} {work['responsibilities']}"
                
                for proj in st.session_state.project_entries:
                    resume_text += f" {proj['name']} {proj['description']}"
                
                for edu in st.session_state.education_entries:
                    resume_text += f" {edu['degree']} {edu['stream']} {edu['institution']}"
                
                # Calculate ATS score
                ats_result = ai_assistant.calculate_ats_score(resume_text, job_desc)
                st.session_state.ats_score = ats_result
                
                # Format check
                all_templates = {**TEMPLATES, **INDIAN_TEMPLATES}
                template_config = all_templates[st.session_state.template]
                resume_html = generate_resume_html(st.session_state, template_config)
                format_check = ATSOptimizer.check_format_compatibility(resume_html)
                
                # Display results
                st.markdown("---")
                
                score = ats_result['score']
                if score >= 75:
                    score_class = "ats-score-excellent"
                    emoji = "🎉"
                elif score >= 50:
                    score_class = "ats-score-good"
                    emoji = "👍"
                else:
                    score_class = "ats-score-poor"
                    emoji = "⚠️"
                
                st.markdown(f"""
                <div class='{score_class}'>
                    <h1>{emoji} ATS Score: {score}/100</h1>
                    <p>{ats_result.get('recommendation', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📈 Detailed Metrics")
                    st.metric("Content Similarity", f"{ats_result.get('similarity', 0)}%")
                    st.metric("Keyword Match", f"{ats_result.get('keyword_match', 0)}%")
                    st.metric("Matched Keywords", f"{ats_result.get('matched_keywords', 0)}/{ats_result.get('total_job_keywords', 0)}")
                    st.metric("Format Compatibility", f"{format_check['score']}%")
                
                with col2:
                    st.markdown("### 🎯 Missing Keywords")
                    if ats_result.get('missing_keywords'):
                        missing = ats_result['missing_keywords'][:10]
                        for kw in missing:
                            st.caption(f"❌ {kw}")
                        st.info("💡 Try incorporating these keywords naturally in your resume")
                    else:
                        st.success("✅ Great keyword coverage!")
                
                # Format recommendations
                if format_check.get('recommendations'):
                    st.markdown("### 📝 Format Recommendations")
                    for rec in format_check['recommendations']:
                        st.warning(f"• {rec}")
                
                # Action verbs suggestion
                st.markdown("### 💪 Power Words to Use")
                action_verbs = ATSOptimizer.get_action_verbs()
                cols = st.columns(6)
                for idx, verb in enumerate(action_verbs[:18]):
                    with cols[idx % 6]:
                        st.caption(f"✓ {verb}")
        else:
            st.error("Please paste a job description to analyze")
    
    # Display previous results if available
    if st.session_state.get('ats_score'):
        st.markdown("---")
        st.info("💡 Scroll up to see your ATS analysis results")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Preview"):
            prev_step()
    with col2:
        if st.button("🏠 Start New Resume"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>✨ Soulvest.ai</strong> - Enterprise-Grade AI-Powered Resume Builder</p>
    <p>🌍 Built for Global Job Seekers | 📧 Support: support@soulvest.ai</p>
    <p style='font-size: 0.9rem;'>© 2026 Soulvest.ai. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
