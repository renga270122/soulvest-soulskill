# app_enhanced.py - Soulvest AI Resume Builder - ResumeGemini Enhanced Version
# Simplified 4-Step Process • Content Library • Live Preview • Multi-Resume Management
import streamlit as st
import streamlit.components.v1 as components
import base64
import tempfile
import json
import os
from datetime import datetime
import time

# Import configurations
from template_config import (TEMPLATES, INDIAN_TEMPLATES, US_TEMPLATES, UK_TEMPLATES, 
                             CANADA_TEMPLATES, AUSTRALIA_TEMPLATES, GERMANY_TEMPLATES, 
                             FRANCE_TEMPLATES, UAE_TEMPLATES, SINGAPORE_TEMPLATES)
from industry_config import INDUSTRY_OPTIONS, INDUSTRY_KEYWORDS, MAJOR_INDIAN_CITIES, INDIAN_STATES
from stream_config import STREAM_OPTIONS
from education_config import DEGREE_OPTIONS
from autocomplete_helper import (JOB_TITLES, TECHNICAL_SKILLS, COMPANIES, CITIES,
                                 create_autocomplete_text_input, get_skill_suggestions)

# Import AI and resume generation modules
from ai_assistant import AIResumeAssistant, ATSOptimizer
from ai_advanced import AdvancedAIAssistant, ResumeScoring
from ats_optimizer_pro import EnterpriseATSOptimizer
from premium_templates import PREMIUM_TEMPLATES, get_template_recommendations
from export_manager import ExportManager
from resume_generator import generate_resume_html
from resume_parser import ResumeParser, parse_uploaded_resume
from sidebar_content import render_enhanced_sidebar
from theme_config import apply_custom_theme
from auth_ui import show_signin_signup_modal, show_user_profile, show_auth_prompt_banner
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
    page_title="Soulvest AI Resume Builder - Build in 5 Minutes",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state early
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = 'User'
if 'mode' not in st.session_state:
    st.session_state.mode = 'home'
if 'show_auth_modal' not in st.session_state:
    st.session_state.show_auth_modal = False

# Apply custom theme
apply_custom_theme()

# Top Navigation Bar (Udemy-style with blue theme)
st.markdown("""
<style>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        border-radius: 0;
        margin: -1rem -1rem 1rem -1rem;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.15);
    }
    .navbar-logo {
        font-size: 1.5rem;
        font-weight: 900;
        color: white;
        margin: 0;
    }
    .navbar-auth {
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }
    .navbar-links {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    .navbar-link {
        color: #ffffff;
        text-decoration: none;
        font-weight: 900;
        font-size: 1rem;
        padding: 0.35rem 0.6rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    .navbar-link:hover {
        background: rgba(255, 255, 255, 0.12);
    }
    .navbar-link-outline {
        border: 1px solid rgba(255, 255, 255, 0.7);
    }
    .navbar-button {
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    .navbar-signin {
        background: transparent;
        color: white;
        border: 1.5px solid white;
    }
    .navbar-signin:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-1px);
    }
    .navbar-signup {
        background: white;
        color: #2563eb;
    }
    .navbar-signup:hover {
        background: #f0f4f8;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
    }
    .navbar-user {
        color: white;
        font-weight: 600;
        margin: 0;
    }
</style>

<div class='navbar'>
    <div class='navbar-logo'>✨ SoulSkill</div>
    <div class='navbar-links'>
        <a class='navbar-link' href='#'>Build Resume</a>
        <a class='navbar-link navbar-link-outline' href='#'>Sign In</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Enhanced CSS for ResumeGemini-like experience
st.markdown("""
<style>
    .main {
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fb 0%, #e8eef7 100%);
    }
    
    /* Primary Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        border: none;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        min-height: 44px; /* Mobile touch target */
        cursor: pointer;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(37, 99, 235, 0.5);
    }
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Mobile-friendly inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        min-height: 44px;
        font-size: 16px; /* Prevents iOS zoom */
        -webkit-appearance: none;
    }
    
    /* Step Indicator */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        padding: 1.5rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .step-item {
        flex: 1;
        text-align: center;
        position: relative;
    }
    .step-item:not(:last-child):after {
        content: '';
        position: absolute;
        top: 20px;
        right: -50%;
        width: 100%;
        height: 2px;
        background: #e0e0e0;
        z-index: -1;
    }
    .step-number {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e0e0e0;
        color: #666;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .step-number.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .step-number.completed {
        background: #10b981;
        color: white;
    }
    .step-label {
        font-size: 0.85rem;
        color: #666;
        font-weight: 500;
    }
    .step-label.active {
        color: #667eea;
        font-weight: 700;
    }
    
    /* Template Gallery */
    .template-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .template-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
        transform: translateY(-4px);
    }
    .template-card.selected {
        border-color: #667eea;
        border-width: 3px;
        background: linear-gradient(135deg, #667eea08 0%, #764ba208 100%);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
    }
    .template-preview {
        width: 100%;
        height: 200px;
        background: #f5f5f5;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        overflow: hidden;
        border: 1px solid #e0e0e0;
        position: relative;
    }
    .template-preview:hover {
        border-color: #667eea;
    }
    .template-name {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.25rem;
        font-size: 0.95rem;
    }
    .template-desc {
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    .ats-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Content Suggestion Box */
    .content-suggestion {
        background: #f3f4f6;
        border-left: 4px solid #2563eb;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .content-suggestion:hover {
        background: #e0e7ff;
        transform: translateX(5px);
    }
    .suggestion-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .suggestion-text {
        font-size: 0.9rem;
        color: #555;
        line-height: 1.5;
    }
    
    /* Resume Preview Panel */
    .preview-panel {
        position: sticky;
        top: 20px;
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        max-height: 80vh;
        overflow-y: auto;
    }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .dashboard-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
    }
    .card-badge {
        padding: 0.25rem 0.75rem;
        background: #2563eb;
        color: white;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Color Picker */
    .color-option {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 3px solid transparent;
    }
    .color-option:hover {
        transform: scale(1.1);
    }
    .color-option.selected {
        border-color: #333;
        box-shadow: 0 0 0 2px white, 0 0 0 4px #333;
    }
    
    /* Info Boxes */
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #10b98115 0%, #059669 15 100%);
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 1.5rem 2rem;
        background: transparent;
        color: white;
        border-radius: 0;
        margin-bottom: 1rem;
        box-shadow: none;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        margin-bottom: 2rem;
    }
    
    /* Stats Section */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #2563eb;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.8rem; }
        .hero-subtitle { font-size: 1rem; }
        .step-indicator { flex-direction: column; }
        .step-item:not(:last-child):after { display: none; }
        .stButton>button { 
            padding: 0.6rem 1rem; 
            font-size: 0.9rem;
        }
        .dashboard-card { padding: 1rem; }
        .template-card { margin-bottom: 1rem; }
    }
    
    /* Mobile-optimized inputs */
    @media (max-width: 768px) {
        textarea, input {
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
    }
    
    /* Auto-save indicator */
    .auto-save-indicator {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize AI Assistants
@st.cache_resource
def get_ai_assistant():
    return AIResumeAssistant()

@st.cache_resource
def get_advanced_ai():
    return AdvancedAIAssistant()

# Reload AI assistants if needed
if 'ai_assistant' not in st.session_state or st.session_state.get('force_ai_reload'):
    if 'force_ai_reload' in st.session_state:
        del st.session_state.force_ai_reload
    st.session_state.ai_assistant = get_ai_assistant()
    st.session_state.advanced_ai = get_advanced_ai()

ai_assistant = st.session_state.ai_assistant
advanced_ai = st.session_state.advanced_ai

# Initialize Session State
def init_session_state():
    defaults = {
        'mode': 'home',  # home, dashboard, builder, coverletter
        'step': 1,  # 1: Template, 2: Fill Details, 3: Customize, 4: Download
        'current_resume_id': None,
        'resumes': {},  # Store multiple resumes
        'profile_type': None,
        'work_entries': [],
        'education_entries': [],
        'certification_entries': [],
        'project_entries': [],
        'language_entries': [],
        'ats_score': None,
        'ai_enabled': ai_assistant.enabled,
        'selected_template': None,
        'color_theme': 'blue',
        'font_family': 'Arial',
        'show_photo': False,
        'resume_completeness': 0,
        'cover_letters': {},
        'cl_company': '',
        'cl_position': '',
        'cl_content': '',
        'show_auth_modal': False,
        'user_authenticated': False,
        'user_email': None,
        'user_name': None,
        'saved_resumes_count': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Import authentication
from auth import get_auth_manager, show_auth_sidebar

# Initialize auth manager early (creates session state keys)
auth_manager = get_auth_manager()

# Enhanced Sidebar with valuable content
render_enhanced_sidebar()

# Show user profile or auth options
show_user_profile()

# Additional sidebar - Universal Navigation
with st.sidebar:
    st.markdown("---")
    
    # Auto-save status
    if st.session_state.mode in ['builder', 'coverletter']:
        st.success("💾 Auto-Save Active")
        st.caption("✓ All changes saved automatically")
    
    # Quick navigation
    st.markdown("### 🚀 Quick Navigation")
    
    if st.button("🏠 Home", use_container_width=True, key="sidebar_home_btn"):
        st.session_state['mode'] = 'home'
        st.rerun()
    
    if st.button("📄 Build Resume", use_container_width=True, key="sidebar_resume_btn"):
        st.session_state['mode'] = 'builder'
        st.session_state['step'] = 1
        st.rerun()
    
    if st.button("✉️ Cover Letter", use_container_width=True, key="sidebar_cl_btn"):
        st.session_state['mode'] = 'coverletter'
        st.rerun()
    
    if st.button("🎓 Masters SOP", use_container_width=True, key="sidebar_masters_btn"):
        st.session_state['mode'] = 'masters'
        st.rerun()
    
    if st.button("📂 Dashboard", use_container_width=True, key="sidebar_dash_btn"):
        st.session_state['mode'] = 'dashboard'
        st.rerun()
    
    if st.button("ℹ️ About", use_container_width=True, key="sidebar_about_btn"):
        st.session_state['mode'] = 'about'
        st.rerun()
    
    if st.button("📧 Contact Us", use_container_width=True, key="sidebar_contact_btn"):
        st.session_state['mode'] = 'contact'
        st.rerun()
    
    # AI Status
    st.markdown("---")
    if st.session_state.ai_enabled:
        st.success("✨ AI: ACTIVE")
        st.caption("Google Gemini enabled")
    else:
        st.warning("⚠️ AI: Offline")
        with st.expander("Enable AI"):
            st.caption("[Get API Key](https://makersuite.google.com/app/apikey)")

# Content Library - Pre-written examples
CONTENT_LIBRARY = {
    "Software Engineer": {
        "summaries": [
            "Results-driven Software Engineer with 5+ years of experience in full-stack development. Expert in React, Node.js, and Python. Successfully delivered 20+ enterprise applications serving 1M+ users.",
            "Innovative Software Developer specializing in cloud-native applications. Proficient in AWS, Docker, and Kubernetes. Led migration of monolithic applications to microservices architecture, improving performance by 40%.",
            "Full Stack Developer with strong foundation in computer science and passion for creating scalable solutions. Experienced in Agile methodologies and continuous integration/deployment pipelines."
        ],
        "work_bullets": [
            "Developed and maintained 15+ RESTful APIs serving 500K+ daily requests with 99.9% uptime",
            "Reduced application load time by 60% through code optimization and implementation of caching strategies",
            "Led team of 5 developers in migration from legacy system to modern React-based architecture",
            "Implemented automated testing suite that increased code coverage from 45% to 85%",
            "Collaborated with cross-functional teams to deliver features ahead of schedule in 90% of sprints",
            "Mentored 3 junior developers, improving team productivity by 25%",
            "Architected microservices infrastructure supporting 2M+ daily active users",
            "Optimized database queries reducing response time by 70% and cost by $50K annually"
        ],
        "skills": ["JavaScript", "React", "Node.js", "Python", "AWS", "Docker", "MongoDB", "PostgreSQL", "Git", "CI/CD", "Agile"]
    },
    "Data Scientist": {
        "summaries": [
            "Data Scientist with 4+ years building ML models that drove $10M+ in revenue. Expert in Python, TensorFlow, and statistical analysis. Published 3 research papers in top-tier conferences.",
            "Analytics-focused Data Scientist specializing in predictive modeling and business intelligence. Reduced customer churn by 25% through advanced ML algorithms. Proficient in Python, R, and SQL.",
            "Machine Learning Engineer with strong background in deep learning and NLP. Built recommendation systems serving 5M+ users. Experienced in model deployment and MLOps practices."
        ],
        "work_bullets": [
            "Developed predictive models that increased sales conversion by 35% generating $2M additional revenue",
            "Built recommendation engine using collaborative filtering serving 1M+ daily recommendations",
            "Reduced model training time by 80% through distributed computing and hyperparameter optimization",
            "Created automated data pipelines processing 10TB+ of data daily",
            "Implemented A/B testing framework that improved experiment velocity by 50%",
            "Led data-driven initiatives that reduced operational costs by $500K annually",
            "Presented insights to C-level executives influencing $5M+ strategic decisions",
            "Mentored team of 4 data analysts in machine learning best practices"
        ],
        "skills": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "SQL", "Spark", "Tableau", "AWS", "Statistics", "ML", "Deep Learning"]
    },
    "Product Manager": {
        "summaries": [
            "Strategic Product Manager with 6+ years launching products that generated $50M+ revenue. Expert in user research, agile methodologies, and data-driven decision making. Successfully led 10+ product launches.",
            "Results-oriented PM specializing in B2B SaaS products. Grew user base from 0 to 100K+ in 2 years. Strong background in stakeholder management and product strategy.",
            "Technical Product Manager with engineering background. Built products used by Fortune 500 companies. Experienced in roadmap planning, sprint management, and cross-functional leadership."
        ],
        "work_bullets": [
            "Launched mobile app that achieved 500K+ downloads and 4.5* rating within 6 months",
            "Defined product roadmap that increased user engagement by 45% and retention by 30%",
            "Led cross-functional team of 15+ across engineering, design, and marketing",
            "Conducted 100+ user interviews to identify pain points and validate product features",
            "Increased monthly recurring revenue by 40% through strategic feature prioritization",
            "Reduced time-to-market by 25% by implementing agile best practices",
            "Managed $2M product budget delivering all milestones on time and under budget",
            "Presented quarterly business reviews to executive team and board of directors"
        ],
        "skills": ["Product Strategy", "Agile", "JIRA", "User Research", "A/B Testing", "SQL", "Analytics", "Roadmapping", "Stakeholder Management"]
    },
    "Marketing Manager": {
        "summaries": [
            "Creative Marketing Manager with 5+ years driving brand growth and customer acquisition. Expertise in digital marketing, SEO, and content strategy. Increased organic traffic by 300% and generated 10K+ qualified leads.",
            "Data-driven Marketing professional specializing in performance marketing and ROI optimization. Managed $1M+ ad budget achieving 5X ROAS. Skilled in Google Ads, Facebook Ads, and marketing automation.",
            "Strategic marketer with proven track record in B2B lead generation. Built marketing funnels that converted 15% of leads to customers. Expert in email marketing, social media, and brand positioning."
        ],
        "work_bullets": [
            "Increased website traffic by 250% through SEO optimization and content marketing strategy",
            "Generated 5000+ qualified leads per quarter through multi-channel campaigns",
            "Managed $500K digital advertising budget achieving 4X return on ad spend",
            "Grew social media following from 10K to 100K+ in 12 months",
            "Launched email nurture campaigns that improved conversion rates by 35%",
            "Reduced customer acquisition cost by 40% through optimization and automation",
            "Led rebranding initiative that increased brand awareness by 60%",
            "Collaborated with sales team to improve lead quality and shorten sales cycle by 20%"
        ],
        "skills": ["Digital Marketing", "SEO", "Google Analytics", "Content Strategy", "Social Media", "Email Marketing", "Google Ads", "HubSpot", "Marketing Automation"]
    },
    "Business Analyst": {
        "summaries": [
            "Detail-oriented Business Analyst with 4+ years translating business needs into technical solutions. Expert in requirements gathering, process optimization, and data analysis. Delivered 15+ successful projects improving operational efficiency by 30%.",
            "Strategic BA specializing in financial services and process improvement. Reduced operational costs by $1M+ through business process reengineering. Proficient in SQL, Tableau, and business modeling.",
            "Technical Business Analyst with strong analytical and communication skills. Bridged gap between business stakeholders and development teams. Managed end-to-end project lifecycle from requirements to UAT."
        ],
        "work_bullets": [
            "Analyzed business requirements for enterprise software serving 10,000+ employees",
            "Identified process inefficiencies saving company $250K annually in operational costs",
            "Created detailed functional specifications for 20+ software development projects",
            "Conducted gap analysis and feasibility studies for system implementations",
            "Developed KPI dashboards providing real-time insights to executive leadership",
            "Led UAT sessions ensuring 95%+ defect-free releases",
            "Facilitated workshops with 50+ stakeholders to gather and prioritize requirements",
            "Improved reporting processes reducing manual work by 15 hours per week"
        ],
        "skills": ["Business Analysis", "Requirements Gathering", "SQL", "Tableau", "Excel", "Process Modeling", "JIRA", "Agile", "Stakeholder Management"]
    },
    "UI/UX Designer": {
        "summaries": [
            "Creative UX Designer with 5+ years crafting intuitive user experiences for web and mobile. Expert in Figma, Adobe XD, and user research. Designed products used by 2M+ users with 4.8* average rating.",
            "User-centered Product Designer specializing in B2B SaaS applications. Increased user satisfaction by 40% and reduced support tickets by 30% through improved UX. Strong in prototyping and usability testing.",
            "Visual and interaction designer with background in psychology and human-computer interaction. Led design systems that improved development efficiency by 50%. Passionate about accessibility and inclusive design."
        ],
        "work_bullets": [
            "Redesigned core user flows increasing conversion rate by 45% and user satisfaction by 35%",
            "Conducted 50+ usability tests to identify pain points and validate design solutions",
            "Created comprehensive design system used across 10+ product teams",
            "Led end-to-end design process from research to high-fidelity prototypes",
            "Collaborated with engineers to ensure pixel-perfect implementation",
            "Reduced user onboarding time by 60% through simplified UX and guided tours",
            "Designed mobile app that achieved 4.7* rating with 100K+ downloads",
            "Mentored 2 junior designers in UX research and design thinking methodologies"
        ],
        "skills": ["Figma", "Adobe XD", "Sketch", "Prototyping", "User Research", "Usability Testing", "Design Systems", "HTML/CSS", "Wireframing"]
    },
    "DevOps Engineer": {
        "summaries": [
            "DevOps Engineer with 6+ years automating infrastructure and CI/CD pipelines. Expert in AWS, Docker, Kubernetes, and Terraform. Reduced deployment time by 80% and improved system reliability to 99.99%.",
            "Cloud Infrastructure specialist with strong background in automation and monitoring. Managed infrastructure serving 10M+ users. Proficient in AWS, Azure, Jenkins, and Infrastructure as Code.",
            "Site Reliability Engineer focused on scalability and performance optimization. Built monitoring systems that reduced incident response time by 70%. Experienced in Kubernetes, Prometheus, and GitOps."
        ],
        "work_bullets": [
            "Designed and implemented CI/CD pipelines reducing deployment time from 4 hours to 15 minutes",
            "Automated infrastructure provisioning with Terraform managing 500+ cloud resources",
            "Reduced AWS costs by 40% through rightsizing and optimization strategies",
            "Built monitoring and alerting system using Prometheus and Grafana improving MTTR by 60%",
            "Migrated monolithic application to Kubernetes increasing scalability and reducing costs by $100K/year",
            "Implemented disaster recovery procedures achieving RPO of 1 hour and RTO of 30 minutes",
            "Led incident response for critical production issues maintaining 99.99% uptime SLA",
            "Automated security scanning in CI/CD pipeline catching 95% of vulnerabilities pre-production"
        ],
        "skills": ["AWS", "Kubernetes", "Docker", "Terraform", "Jenkins", "CI/CD", "Linux", "Python", "Ansible", "Prometheus", "GitLab"]
    },
    "Sales Manager": {
        "summaries": [
            "Results-driven Sales Manager with 8+ years exceeding revenue targets. Built and led teams of 10+ reps achieving 150% of quota. Expert in B2B sales, CRM systems, and strategic account management.",
            "Strategic sales leader with proven track record of driving growth in competitive markets. Increased territory revenue by 200% in 2 years. Strong in relationship building, negotiation, and sales enablement.",
            "Dynamic Sales Manager specializing in enterprise solutions. Closed $10M+ in deals annually. Skilled in consultative selling, pipeline management, and cross-functional collaboration."
        ],
        "work_bullets": [
            "Exceeded sales quota by 175% generating $5M in new revenue annually",
            "Built and managed sales team of 12 reps achieving team quota of 160%",
            "Closed 3 enterprise deals worth $1M+ each through strategic account management",
            "Reduced sales cycle by 30% through improved qualification and sales processes",
            "Implemented CRM best practices increasing pipeline visibility and forecast accuracy to 95%",
            "Conducted 50+ product demos and presentations converting 40% to paying customers",
            "Developed sales playbooks and training programs improving new rep ramp time by 40%",
            "Expanded customer base by 250% through targeted prospecting and lead generation campaigns"
        ],
        "skills": ["B2B Sales", "Salesforce", "Account Management", "Negotiation", "Lead Generation", "CRM", "Sales Strategy", "Presentation"]
    },
    "HR Manager": {
        "summaries": [
            "Strategic HR Manager with 7+ years building high-performing teams and fostering positive culture. Expert in talent acquisition, performance management, and employee relations. Reduced turnover by 35% and improved engagement scores to 85%.",
            "People-focused HR professional specializing in organizational development and change management. Managed HR operations for 500+ employees. Strong in HRIS, compliance, and benefits administration.",
            "Results-oriented Human Resources leader with expertise in talent strategy and workforce planning. Built recruitment programs that reduced time-to-hire by 50%. Passionate about diversity, equity, and inclusion."
        ],
        "work_bullets": [
            "Reduced employee turnover by 35% through improved retention strategies and engagement programs",
            "Built recruitment pipeline hiring 100+ employees annually with 95% retention after first year",
            "Implemented performance management system increasing employee productivity by 25%",
            "Conducted salary benchmarking and restructured compensation reducing pay equity gaps",
            "Led diversity and inclusion initiatives increasing representation of underrepresented groups by 40%",
            "Managed employee relations cases ensuring compliance and maintaining positive work environment",
            "Redesigned onboarding program improving new hire satisfaction scores by 45%",
            "Negotiated with benefits providers saving company $200K annually while improving coverage"
        ],
        "skills": ["Talent Acquisition", "HRIS", "Performance Management", "Employee Relations", "Compliance", "Benefits Administration", "DEI", "Payroll"]
    },
    "Financial Analyst": {
        "summaries": [
            "Financial Analyst with 5+ years providing data-driven insights for strategic decision making. Expert in financial modeling, forecasting, and variance analysis. Identified cost savings opportunities worth $2M+ annually.",
            "Detail-oriented finance professional specializing in FP&A and budget management. Managed annual budget of $50M+ with 98% accuracy. Proficient in Excel, SQL, and Tableau.",
            "Strategic analyst with strong background in investment analysis and risk management. Built financial models supporting $100M+ in business decisions. CFA Level II candidate."
        ],
        "work_bullets": [
            "Built financial models and forecasts with 95%+ accuracy driving $50M+ investment decisions",
            "Identified cost reduction opportunities saving company $2M annually through variance analysis",
            "Automated monthly reporting processes reducing reporting time from 5 days to 1 day",
            "Conducted financial analysis for 3 M&A transactions valued at $200M+ total",
            "Created executive dashboards in Tableau providing real-time visibility into KPIs",
            "Led budgeting process for department of 200+ employees managing $30M annual budget",
            "Performed ROI analysis on capital projects helping prioritize $10M in investments",
            "Presented quarterly financial reviews to C-suite executives and board of directors"
        ],
        "skills": ["Financial Modeling", "Excel", "SQL", "Tableau", "FP&A", "Budgeting", "Forecasting", "Variance Analysis", "Bloomberg"]
    },
    "Content Writer": {
        "summaries": [
            "Creative Content Writer with 4+ years crafting engaging copy for web, social media, and email. Written 500+ articles generating 5M+ views. Expert in SEO, storytelling, and content strategy.",
            "Versatile writer specializing in B2B SaaS and technology content. Increased organic traffic by 200% through SEO-optimized blog posts. Strong in research, editing, and content marketing.",
            "Strategic content creator with background in journalism and digital marketing. Built content library of 300+ pieces supporting lead generation goals. Skilled in WordPress, HubSpot, and Google Analytics."
        ],
        "work_bullets": [
            "Wrote 500+ blog posts and articles generating 5M+ views and 50K+ leads",
            "Increased organic traffic by 200% through SEO-optimized content strategy",
            "Created email campaigns with 35% open rate and 8% click-through rate",
            "Managed content calendar publishing 4-5 high-quality pieces per week",
            "Conducted keyword research and competitor analysis informing content strategy",
            "Collaborated with design team creating 100+ infographics and visual assets",
            "Edited and proofread content ensuring consistency with brand voice and style guide",
            "Achieved #1 Google rankings for 20+ target keywords driving qualified traffic"
        ],
        "skills": ["Content Writing", "SEO", "Copywriting", "WordPress", "HubSpot", "Google Analytics", "Email Marketing", "Social Media"]
    },
    "Graphic Designer": {
        "summaries": [
            "Creative Graphic Designer with 5+ years designing visual content for digital and print. Created 1000+ designs for brands, marketing campaigns, and social media. Expert in Adobe Creative Suite and brand identity.",
            "Visual designer specializing in brand identity and marketing collateral. Designed logos and brand guidelines for 50+ clients. Strong in illustration, typography, and layout design.",
            "Multi-disciplinary designer with expertise in UI/UX and motion graphics. Created designs that increased engagement by 60%. Proficient in Figma, Adobe CC, and After Effects."
        ],
        "work_bullets": [
            "Designed 1000+ graphics for social media generating 10M+ impressions",
            "Created brand identity and style guide for 50+ clients across various industries",
            "Designed marketing materials for campaigns that generated $5M+ in revenue",
            "Collaborated with marketing team on 20+ product launches and promotional campaigns",
            "Maintained brand consistency across all visual touchpoints and channels",
            "Reduced design turnaround time by 40% through efficient workflows and templates",
            "Led redesign of company website improving user engagement by 50%",
            "Mentored 2 junior designers in Adobe Creative Suite and design principles"
        ],
        "skills": ["Adobe Photoshop", "Illustrator", "InDesign", "Figma", "Brand Identity", "Typography", "Layout Design", "Print Design"]
    },
    "Customer Success Manager": {
        "summaries": [
            "Customer Success Manager with 5+ years driving retention and expansion in SaaS. Managed portfolio of 100+ accounts worth $10M+ ARR. Achieved 95% retention rate and 150% net revenue retention.",
            "Client-focused CSM specializing in enterprise accounts and strategic partnerships. Reduced churn by 40% through proactive engagement. Expert in onboarding, training, and relationship building.",
            "Results-driven success professional with background in account management and support. Upsold $2M+ in additional services. Strong in CRM, data analysis, and customer advocacy."
        ],
        "work_bullets": [
            "Managed portfolio of 100+ customer accounts representing $10M+ in annual recurring revenue",
            "Achieved 95% customer retention rate and 150% net revenue retention",
            "Reduced customer churn by 40% through proactive engagement and success planning",
            "Conducted 200+ onboarding sessions and training webinars for new customers",
            "Identified upsell opportunities generating $2M+ in expansion revenue",
            "Built customer health scoring system to identify at-risk accounts early",
            "Gathered customer feedback influencing product roadmap and feature prioritization",
            "Created help center and knowledge base reducing support tickets by 30%"
        ],
        "skills": ["Customer Success", "Account Management", "Salesforce", "Onboarding", "SaaS", "Retention", "Upselling", "CRM"]
    },
    "Project Manager": {
        "summaries": [
            "Certified Project Manager (PMP) with 7+ years delivering complex projects on time and under budget. Led 30+ projects worth $20M+ total. Expert in Agile, Scrum, and stakeholder management.",
            "Results-oriented PM specializing in software development and IT projects. Managed cross-functional teams of 20+ members. Strong in risk management, resource planning, and process improvement.",
            "Strategic project leader with track record of turning around failing projects. Delivered projects with 98% on-time completion rate. Skilled in MS Project, JIRA, and change management."
        ],
        "work_bullets": [
            "Led 30+ projects from initiation to closure delivering $20M+ in business value",
            "Managed cross-functional teams of 20+ stakeholders across engineering, design, and marketing",
            "Achieved 98% on-time project delivery rate and maintained average 15% under budget",
            "Implemented Agile methodologies reducing project delivery time by 35%",
            "Mitigated project risks through proactive planning and stakeholder communication",
            "Created project dashboards providing real-time visibility to executives and stakeholders",
            "Conducted post-project reviews identifying lessons learned and process improvements",
            "Managed project budgets totaling $5M+ annually with 100% financial accuracy"
        ],
        "skills": ["Project Management", "PMP", "Agile", "Scrum", "JIRA", "MS Project", "Risk Management", "Stakeholder Management"]
    },
    "Cybersecurity Analyst": {
        "summaries": [
            "Cybersecurity Analyst with 5+ years protecting enterprise systems and data. Prevented security breaches saving company $10M+ in potential losses. Expert in threat detection, incident response, and security frameworks.",
            "Security professional specializing in penetration testing and vulnerability assessment. Identified and remediated 500+ security vulnerabilities. Certified in CISSP, CEH, and CompTIA Security+.",
            "Proactive security analyst with background in network security and forensics. Built security monitoring system detecting threats in real-time. Strong in SIEM, firewalls, and security policies."
        ],
        "work_bullets": [
            "Monitored security systems protecting infrastructure serving 100K+ users",
            "Identified and remediated 500+ security vulnerabilities preventing potential breaches",
            "Conducted penetration tests and security audits for 20+ critical applications",
            "Responded to 50+ security incidents with average resolution time of 2 hours",
            "Implemented security awareness training reducing phishing click rate by 70%",
            "Built SIEM dashboards providing real-time visibility into security events",
            "Ensured compliance with SOC 2, ISO 27001, and GDPR security standards",
            "Developed incident response playbooks reducing mean time to respond by 60%"
        ],
        "skills": ["Cybersecurity", "SIEM", "Penetration Testing", "Incident Response", "CISSP", "Network Security", "Firewalls", "Compliance"]
    }
}

# Helper Functions
def auto_save_field(field_name, value):
    """Auto-save field value to session state"""
    st.session_state[field_name] = value
    return value

def render_step_indicator(current_step):
    """Render 4-step progress indicator"""
    steps = [
        {"num": 1, "label": "Choose Template", "icon": "🎨"},
        {"num": 2, "label": "Fill Details", "icon": "📝"},
        {"num": 3, "label": "Customize", "icon": "✨"},
        {"num": 4, "label": "Download", "icon": "📥"}
    ]
    
    cols = st.columns(4)
    for idx, step in enumerate(steps):
        with cols[idx]:
            status = ""
            if step["num"] < current_step:
                status = "completed"
            elif step["num"] == current_step:
                status = "active"
            
            badge_class = "completed" if status == "completed" else ("active" if status == "active" else "")
            label_class = "active" if status == "active" else ""
            
            st.markdown(f"""
            <div class='step-item'>
                <div class='step-number {badge_class}'>{step['icon'] if status == 'completed' else step['num']}</div>
                <div class='step-label {label_class}'>{step['label']}</div>
            </div>
            """, unsafe_allow_html=True)

def get_content_suggestions(job_role, content_type):
    """Get pre-written content suggestions for a job role"""
    if job_role in CONTENT_LIBRARY:
        return CONTENT_LIBRARY[job_role].get(content_type, [])
    return []

def calculate_completeness():
    """Calculate resume completeness percentage"""
    required_fields = [
        'full_name', 'email', 'phone', 'city',
        'summary', 'tech_skills'
    ]
    completed = sum(1 for field in required_fields if st.session_state.get(field))
    
    # Add work experience check
    if st.session_state.get('work_entries'):
        completed += 1
    
    # Add education check
    if st.session_state.get('education_entries'):
        completed += 1
    
    total = len(required_fields) + 2
    return int((completed / total) * 100)

def get_template_preview_html(template_config, template_id):
    """Generate actual miniature resume preview with sample data"""
    sample_data = get_sample_resume_data()
    
    # Get template colors
    primary_color = template_config.get('color', '#667eea')
    font_family = template_config.get('font', 'Arial')
    
    # Get work experience data properly
    work_exp = sample_data.get('work_entries', [])
    education = sample_data.get('education_entries', [])
    skills = sample_data.get('tech_skills', 'JavaScript, React, Python, AWS')
    
    # Generate actual resume preview in miniature
    preview_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: {font_family}, Arial, sans-serif; padding: 8px; background: white; font-size: 5px; line-height: 1.3; }}
            .header {{ text-align: center; border-bottom: 1.5px solid {primary_color}; padding-bottom: 4px; margin-bottom: 5px; }}
            .name {{ font-size: 9px; font-weight: bold; color: {primary_color}; margin-bottom: 2px; }}
            .title {{ font-size: 5px; color: #666; margin-bottom: 2px; }}
            .contact {{ font-size: 4px; color: #666; }}
            .section {{ margin-bottom: 5px; }}
            .section-title {{ font-size: 6px; font-weight: bold; color: {primary_color}; border-bottom: 1px solid {primary_color}; padding-bottom: 1px; margin-bottom: 2px; text-transform: uppercase; }}
            .section-content {{ font-size: 4px; color: #333; line-height: 1.4; }}
            .job-title {{ font-size: 5px; font-weight: bold; color: #333; margin-bottom: 1px; }}
            .company {{ font-size: 4px; color: #666; margin-bottom: 1px; }}
            .skills {{ display: flex; flex-wrap: wrap; gap: 2px; }}
            .skill {{ background: #f0f0f0; padding: 1px 3px; border-radius: 2px; font-size: 4px; }}
            ul {{ margin-left: 5px; }}
            li {{ font-size: 4px; margin-bottom: 0.5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="name">{sample_data['full_name']}</div>
            <div class="title">{sample_data.get('job_title_target', 'Professional')}</div>
            <div class="contact">{sample_data['email']} • {sample_data['phone']} • {sample_data['city']}</div>
        </div>
        
        <div class="section">
            <div class="section-title">Summary</div>
            <div class="section-content">{sample_data['summary'][:120]}...</div>
        </div>
        
        <div class="section">
            <div class="section-title">Skills</div>
            <div class="skills">
                {''.join([f'<span class="skill">{skill.strip()}</span>' for skill in skills.split(',')[:6]])}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Experience</div>
            {''.join([f'''<div style="margin-bottom: 3px;">
                <div class="job-title">{exp.get('title', 'Position')}</div>
                <div class="company">{exp.get('company', 'Company')} • {exp.get('start_date', '2020')} - {exp.get('end_date', 'Present')}</div>
                <ul>{''.join([f'<li>{resp.strip()[:80]}...</li>' for resp in exp.get('responsibilities', '').split(chr(10))[:2] if resp.strip()])}</ul>
            </div>''' for exp in work_exp[:2]])}
        </div>
        
        <div class="section">
            <div class="section-title">Education</div>
            {''.join([f'''<div>
                <div class="job-title">{edu.get('degree', 'Degree')} - {edu.get('stream', 'Field')}</div>
                <div class="company">{edu.get('institution', 'University')} • {edu.get('year', '2020')}</div>
            </div>''' for edu in education[:1]])}
        </div>
    </body>
    </html>
    """
    return preview_html

def get_sample_resume_data():
    """Get sample resume data for template preview"""
    return {
        'full_name': 'John Doe',
        'email': 'john.doe@email.com',
        'phone': '+1 (555) 123-4567',
        'city': 'San Francisco',
        'linkedin': 'linkedin.com/in/johndoe',
        'job_title_target': 'Senior Software Engineer',
        'summary': 'Results-driven Software Engineer with 5+ years of experience in full-stack development. Expert in React, Node.js, and Python. Successfully delivered 20+ enterprise applications.',
        'tech_skills': 'JavaScript, React, Node.js, Python, AWS, Docker, PostgreSQL',
        'soft_skills': 'Leadership, Communication, Problem Solving',
        'work_entries': [
            {
                'title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'start_date': 'Jan 2020',
                'end_date': 'Present',
                'responsibilities': '• Led development of cloud-based platform serving 100K+ users\n• Reduced application load time by 60% through optimization\n• Mentored team of 5 junior developers'
            },
            {
                'title': 'Software Engineer',
                'company': 'StartupXYZ',
                'start_date': 'Jun 2018',
                'end_date': 'Dec 2019',
                'responsibilities': '• Developed RESTful APIs with 99.9% uptime\n• Implemented CI/CD pipelines improving deployment efficiency'
            }
        ],
        'education_entries': [
            {
                'degree': 'Bachelor of Science',
                'stream': 'Computer Science',
                'institution': 'University of California',
                'year': '2018',
                'score': '3.8 GPA'
            }
        ],
        'project_entries': [],
        'certification_entries': [],
        'language_entries': []
    }

def calculate_completeness():
    """Calculate resume completeness percentage"""
    required_fields = [
        'full_name', 'email', 'phone', 'city',
        'summary', 'tech_skills'
    ]
    completed = sum(1 for field in required_fields if st.session_state.get(field))
    
    # Add work experience check
    if st.session_state.get('work_entries'):
        completed += 1
    
    # Add education check
    if st.session_state.get('education_entries'):
        completed += 1
    
    total = len(required_fields) + 2
    return int((completed / total) * 100)

# MAIN APP NAVIGATION
if st.session_state.mode == 'home':
    # Show auth modal if requested
    if st.session_state.get('show_auth_modal', False):
        show_signin_signup_modal()
    else:
        # Landing Page - Hero Section with Welcome Banner
        col_left, col_center, col_right = st.columns([1, 2, 1])
        
        # Left side - Resume Preview Mockup
        with col_left:
            st.markdown("""
            <div style='text-align: left; padding: 1.4rem 1.2rem; background: linear-gradient(180deg, #ffffff 0%, #f6f9ff 100%); border-radius: 16px; min-height: 320px; border: 1px solid rgba(37, 99, 235, 0.2); box-shadow: 0 12px 28px rgba(37, 99, 235, 0.14);'>
                <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;'>
                    <span style='background: #e0e7ff; color: #1e3a8a; font-size: 0.72rem; font-weight: 800; padding: 0.25rem 0.55rem; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.6px;'>ATS Friendly</span>
                    <span style='color: #2563eb; font-size: 0.75rem; font-weight: 800;'>★ 4.9</span>
                </div>
                <div style='display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem;'>
                    <div style='width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%); color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: 800;'>PR</div>
                    <div>
                        <h3 style='color: #1e3a8a; font-size: 1.1rem; font-weight: 800; margin: 0;'>Priya Rao</h3>
                        <p style='color: #4a5568; font-size: 0.82rem; font-weight: 600; margin: 0.1rem 0 0 0;'>Data Analyst • Bengaluru</p>
                    </div>
                </div>
                <div style='height: 1px; background: rgba(37, 99, 235, 0.15); margin: 0.7rem 0;'></div>
                <p style='color: #1e3a8a; font-size: 0.85rem; font-weight: 800; margin: 0 0 0.35rem 0;'>Highlights</p>
                <ul style='color: #4a5568; font-size: 0.78rem; margin: 0; padding-left: 1rem; line-height: 1.6;'>
                    <li>SQL • Python • Power BI</li>
                    <li>Built 12+ dashboards</li>
                    <li>ATS‑optimized keywords</li>
                </ul>
                <div style='margin-top: 0.7rem;'>
                    <div style='height: 6px; background: #e6edff; border-radius: 999px; overflow: hidden; margin-bottom: 0.35rem;'>
                        <div style='width: 78%; height: 100%; background: linear-gradient(90deg, #2563eb, #1e3a8a);'></div>
                    </div>
                    <p style='color: #4a5568; font-size: 0.72rem; font-weight: 700; margin: 0;'>Keyword Match: 78%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Center - Hero Title + Welcome Banner Combined
        with col_center:
            st.markdown("""
            <div style='text-align: center; padding: 1.6rem 1.6rem 2.1rem 1.6rem; background: linear-gradient(135deg, #eaf2ff 0%, #dfe9ff 50%, #f6f9ff 100%); border-radius: 18px; border: 1px solid rgba(37, 99, 235, 0.25); box-shadow: 0 14px 30px rgba(30, 58, 138, 0.18);'>
                <p style='color: #1e3a8a; font-size: 2.4rem; font-weight: 900; margin: 0 0 0.15rem 0;'>Welcome to SoulSkill! 👋</p>
                <h1 style='color: #1e3a8a; font-size: 2.35rem; font-weight: 900; margin: 0 0 0.5rem 0; letter-spacing: 0.2px;'>Build Your Resume in as little as 5 minutes</h1>
                <p style='color: #3b4a6b; font-size: 1.02rem; font-weight: 600; margin: 0; line-height: 1.55;'>Build professional resumes, cover letters, and more with AI-powered assistance.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Right side - Resume Preview Mockup
        with col_right:
            st.markdown("""
            <div style='text-align: left; padding: 1.4rem 1.2rem; background: linear-gradient(180deg, #ffffff 0%, #f6f9ff 100%); border-radius: 16px; min-height: 320px; border: 1px solid rgba(37, 99, 235, 0.2); box-shadow: 0 12px 28px rgba(37, 99, 235, 0.14);'>
                <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;'>
                    <span style='background: #e0e7ff; color: #1e3a8a; font-size: 0.72rem; font-weight: 800; padding: 0.25rem 0.55rem; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.6px;'>Recruiter Ready</span>
                    <span style='color: #2563eb; font-size: 0.75rem; font-weight: 800;'>★ 4.8</span>
                </div>
                <div style='display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem;'>
                    <div style='width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: 800;'>AB</div>
                    <div>
                        <h3 style='color: #1e3a8a; font-size: 1.1rem; font-weight: 800; margin: 0;'>Aiden Brooks</h3>
                        <p style='color: #4a5568; font-size: 0.82rem; font-weight: 600; margin: 0.1rem 0 0 0;'>Product Manager • Austin</p>
                    </div>
                </div>
                <div style='height: 1px; background: rgba(37, 99, 235, 0.15); margin: 0.7rem 0;'></div>
                <p style='color: #1e3a8a; font-size: 0.85rem; font-weight: 800; margin: 0 0 0.35rem 0;'>Highlights</p>
                <ul style='color: #4a5568; font-size: 0.78rem; margin: 0; padding-left: 1rem; line-height: 1.6;'>
                    <li>Roadmaps • OKRs • GTM</li>
                    <li>Led 4 product launches</li>
                    <li>ATS‑friendly layout</li>
                </ul>
                <div style='margin-top: 0.7rem;'>
                    <div style='height: 6px; background: #e6edff; border-radius: 999px; overflow: hidden; margin-bottom: 0.35rem;'>
                        <div style='width: 84%; height: 100%; background: linear-gradient(90deg, #22c55e, #16a34a);'></div>
                    </div>
                    <p style='color: #4a5568; font-size: 0.72rem; font-weight: 700; margin: 0;'>Formatting Score: 84%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Quick steps to build trust
        step1, step2, step3 = st.columns(3)
        with step1:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: #ffffff; border-radius: 14px; border: 1px solid rgba(37, 99, 235, 0.18); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.1);'>
                <div style='font-size: 1.4rem;'>📝</div>
                <p style='color:#1e3a8a; font-weight:800; margin:0.35rem 0 0.2rem 0;'>Fill Details</p>
                <p style='color:#4a5568; font-size:0.8rem; margin:0;'>Guided sections in minutes</p>
            </div>
            """, unsafe_allow_html=True)
        with step2:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: #ffffff; border-radius: 14px; border: 1px solid rgba(37, 99, 235, 0.18); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.1);'>
                <div style='font-size: 1.4rem;'>✨</div>
                <p style='color:#1e3a8a; font-weight:800; margin:0.35rem 0 0.2rem 0;'>AI Suggestions</p>
                <p style='color:#4a5568; font-size:0.8rem; margin:0;'>Instant wording improvements</p>
            </div>
            """, unsafe_allow_html=True)
        with step3:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: #ffffff; border-radius: 14px; border: 1px solid rgba(37, 99, 235, 0.18); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.1);'>
                <div style='font-size: 1.4rem;'>📄</div>
                <p style='color:#1e3a8a; font-weight:800; margin:0.35rem 0 0.2rem 0;'>Download PDF</p>
                <p style='color:#4a5568; font-size:0.8rem; margin:0;'>ATS‑ready templates</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Auth buttons for guests
        if not st.session_state.user_authenticated:

            # Main CTA Button
            st.markdown("""
            <div style='text-align: center; margin-top: 1.2rem;'>
                <button onclick="window.location.href='#'" style='padding: 0.85rem 2rem; background: #ffffff; color: #1e3a8a; border: 3px solid #1e3a8a; border-radius: 10px; font-size: 1.08rem; font-weight: 900; cursor: pointer; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15); transition: all 0.3s ease;'>🚀 Build Your Resume For Free</button>
                <p style='text-align:center; color:#4a5568; font-weight:600; font-size:0.85rem; margin-top:0.5rem;'>No credit card required</p>
            </div>
            """, unsafe_allow_html=True)

            # Additional Auth Options
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("""
                <div style='text-align: center;'>
                    <button onclick="window.location.href='#'" style='padding: 0.65rem 1.5rem; background: #ffffff; color: #1e3a8a; border: 3px solid #1e3a8a; border-radius: 8px; font-size: 1rem; font-weight: 900; cursor: pointer; width: 100%; box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);'>🔐 Sign In</button>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown("""
                <div style='text-align: center;'>
                    <button onclick="window.location.href='#'" style='padding: 0.65rem 1.5rem; background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%); color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: 700; cursor: pointer; width: 100%; box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);'>✨ Create Account</button>
                </div>
                """, unsafe_allow_html=True)
            with col_c:
                st.markdown("""
                <div style='text-align: center;'>
                    <button onclick="window.location.href='#'" style='padding: 0.65rem 1.5rem; background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%); color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: 700; cursor: pointer; width: 100%; box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);'>👤 Continue as Guest</button>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Hero Section + Welcome for logged-in users with side quotes
            col_left, col_center, col_right = st.columns([1, 2, 1])
            
            # Left side - Resume Preview Mockup
            with col_left:
                st.markdown("""
                <div style='text-align: left; padding: 1.4rem 1.2rem; background: linear-gradient(180deg, #ffffff 0%, #f6f9ff 100%); border-radius: 16px; min-height: 320px; border: 1px solid rgba(37, 99, 235, 0.2); box-shadow: 0 12px 28px rgba(37, 99, 235, 0.14);'>
                    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;'>
                        <span style='background: #e0e7ff; color: #1e3a8a; font-size: 0.72rem; font-weight: 800; padding: 0.25rem 0.55rem; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.6px;'>ATS Friendly</span>
                        <span style='color: #2563eb; font-size: 0.75rem; font-weight: 800;'>★ 4.9</span>
                    </div>
                    <div style='display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem;'>
                        <div style='width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%); color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: 800;'>PR</div>
                        <div>
                            <h3 style='color: #1e3a8a; font-size: 1.1rem; font-weight: 800; margin: 0;'>Priya Rao</h3>
                            <p style='color: #4a5568; font-size: 0.82rem; font-weight: 600; margin: 0.1rem 0 0 0;'>Data Analyst • Bengaluru</p>
                        </div>
                    </div>
                    <div style='height: 1px; background: rgba(37, 99, 235, 0.15); margin: 0.7rem 0;'></div>
                    <p style='color: #1e3a8a; font-size: 0.85rem; font-weight: 800; margin: 0 0 0.35rem 0;'>Highlights</p>
                    <ul style='color: #4a5568; font-size: 0.78rem; margin: 0; padding-left: 1rem; line-height: 1.6;'>
                        <li>SQL • Python • Power BI</li>
                        <li>Built 12+ dashboards</li>
                        <li>ATS‑optimized keywords</li>
                    </ul>
                    <div style='margin-top: 0.7rem;'>
                        <div style='height: 6px; background: #e6edff; border-radius: 999px; overflow: hidden; margin-bottom: 0.35rem;'>
                            <div style='width: 78%; height: 100%; background: linear-gradient(90deg, #2563eb, #1e3a8a);'></div>
                        </div>
                        <p style='color: #4a5568; font-size: 0.72rem; font-weight: 700; margin: 0;'>Keyword Match: 78%</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Center - Hero Title + Welcome
            with col_center:
                st.markdown(f"""
                <div style='text-align: center; padding: 1.6rem 1.6rem 2.1rem 1.6rem; background: linear-gradient(135deg, #eaf2ff 0%, #dfe9ff 50%, #f6f9ff 100%); border-radius: 18px; border: 1px solid rgba(37, 99, 235, 0.25); box-shadow: 0 14px 30px rgba(30, 58, 138, 0.18);'>
                    <h2 style='color: #1e3a8a; font-size: 2.2rem; font-weight: 900; margin: 0 0 0.2rem 0;'>👋 Welcome back, {st.session_state.get('user_name', 'User')}!</h2>
                    <h1 style='color: #1e3a8a; font-size: 2.35rem; font-weight: 900; margin: 0 0 0.5rem 0; letter-spacing: 0.2px;'>Build Your Resume in as little as 5 minutes</h1>
                    <p style='color: #3b4a6b; font-size: 1rem; font-weight: 600; margin: 0; line-height: 1.55;'>Ready to create amazing resumes?</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Right side - Resume Preview Mockup
            with col_right:
                st.markdown("""
                <div style='text-align: left; padding: 1.4rem 1.2rem; background: linear-gradient(180deg, #ffffff 0%, #f6f9ff 100%); border-radius: 16px; min-height: 320px; border: 1px solid rgba(37, 99, 235, 0.2); box-shadow: 0 12px 28px rgba(37, 99, 235, 0.14);'>
                    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;'>
                        <span style='background: #e0e7ff; color: #1e3a8a; font-size: 0.72rem; font-weight: 800; padding: 0.25rem 0.55rem; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.6px;'>Recruiter Ready</span>
                        <span style='color: #2563eb; font-size: 0.75rem; font-weight: 800;'>★ 4.8</span>
                    </div>
                    <div style='display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem;'>
                        <div style='width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: 800;'>AB</div>
                        <div>
                            <h3 style='color: #1e3a8a; font-size: 1.1rem; font-weight: 800; margin: 0;'>Aiden Brooks</h3>
                            <p style='color: #4a5568; font-size: 0.82rem; font-weight: 600; margin: 0.1rem 0 0 0;'>Product Manager • Austin</p>
                        </div>
                    </div>
                    <div style='height: 1px; background: rgba(37, 99, 235, 0.15); margin: 0.7rem 0;'></div>
                    <p style='color: #1e3a8a; font-size: 0.85rem; font-weight: 800; margin: 0 0 0.35rem 0;'>Highlights</p>
                    <ul style='color: #4a5568; font-size: 0.78rem; margin: 0; padding-left: 1rem; line-height: 1.6;'>
                        <li>Roadmaps • OKRs • GTM</li>
                        <li>Led 4 product launches</li>
                        <li>ATS‑friendly layout</li>
                    </ul>
                    <div style='margin-top: 0.7rem;'>
                        <div style='height: 6px; background: #e6edff; border-radius: 999px; overflow: hidden; margin-bottom: 0.35rem;'>
                            <div style='width: 84%; height: 100%; background: linear-gradient(90deg, #22c55e, #16a34a);'></div>
                        </div>
                        <p style='color: #4a5568; font-size: 0.72rem; font-weight: 700; margin: 0;'>Formatting Score: 84%</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Quick steps to build trust
            step1, step2, step3 = st.columns(3)
            with step1:
                st.markdown("""
                <div style='text-align: center; padding: 1rem; background: #ffffff; border-radius: 14px; border: 1px solid rgba(37, 99, 235, 0.18); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.1);'>
                    <div style='font-size: 1.4rem;'>📝</div>
                    <p style='color:#1e3a8a; font-weight:800; margin:0.35rem 0 0.2rem 0;'>Fill Details</p>
                    <p style='color:#4a5568; font-size:0.8rem; margin:0;'>Guided sections in minutes</p>
                </div>
                """, unsafe_allow_html=True)
            with step2:
                st.markdown("""
                <div style='text-align: center; padding: 1rem; background: #ffffff; border-radius: 14px; border: 1px solid rgba(37, 99, 235, 0.18); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.1);'>
                    <div style='font-size: 1.4rem;'>✨</div>
                    <p style='color:#1e3a8a; font-weight:800; margin:0.35rem 0 0.2rem 0;'>AI Suggestions</p>
                    <p style='color:#4a5568; font-size:0.8rem; margin:0;'>Instant wording improvements</p>
                </div>
                """, unsafe_allow_html=True)
            with step3:
                st.markdown("""
                <div style='text-align: center; padding: 1rem; background: #ffffff; border-radius: 14px; border: 1px solid rgba(37, 99, 235, 0.18); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.1);'>
                    <div style='font-size: 1.4rem;'>📄</div>
                    <p style='color:#1e3a8a; font-weight:800; margin:0.35rem 0 0.2rem 0;'>Download PDF</p>
                    <p style='color:#4a5568; font-size:0.8rem; margin:0;'>ATS‑ready templates</p>
                </div>
                """, unsafe_allow_html=True)

            cta_left, cta_center, cta_right = st.columns([1, 2, 1])
            with cta_center:
                if st.button("🚀 Build Your Resume For Free", use_container_width=True, key="hero_build_free_auth", type="primary"):
                    st.session_state['mode'] = 'builder'
                    st.session_state['step'] = 1
                    st.rerun()
                st.markdown("<p style='text-align:center; color:#4a5568; font-weight:600; font-size:0.85rem; margin-top:0.35rem;'>No credit card required</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA Buttons (Only for signed-in users)
    if st.session_state.user_authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Use unique keys and direct state changes
            if st.button("🚀 Build Resume For Free", use_container_width=True, type="primary", key="home_build_btn"):
                st.session_state['mode'] = 'builder'
                st.session_state['step'] = 1
                st.rerun()
            
            if st.button("✉️ Create Cover Letter", use_container_width=True, key="home_coverletter_btn"):
                st.session_state['mode'] = 'coverletter'
                st.rerun()
            
            if st.button("🎓 Masters Application Letter", use_container_width=True, key="home_masters_btn"):
                st.session_state['mode'] = 'masters'
                st.rerun()
            
            if st.button("📂 My Resumes Dashboard", use_container_width=True, key="home_dashboard_btn"):
                st.session_state['mode'] = 'dashboard'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Resume Upload Feature - Auto-Fill (Only for signed-in users)
    if st.session_state.user_authenticated:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h3 style='font-weight: 800; color: #2d3748; font-size: 1.75rem;'><strong>📤 Have an Existing Resume?</strong></h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-weight: 600; color: #4a5568; font-size: 1.05rem;'><strong>Upload your current resume (PDF, DOCX, TXT) and we'll auto-fill the details for you!</strong></p>", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Upload your resume",
                type=['pdf', 'docx', 'txt'],
                key="home_resume_upload",
                help="We'll extract your information and auto-fill the resume builder"
            )
            
            if uploaded_file:
                with st.spinner("🤖 Analyzing your resume with AI..."):
                    try:
                        # Parse the resume
                        api_key = st.session_state.get('gemini_api_key')
                        parsed_data = parse_uploaded_resume(uploaded_file, api_key=api_key)
                        
                        # Auto-fill session state
                        parser = ResumeParser(api_key=api_key)
                        parser.auto_fill_session_state(parsed_data, st.session_state)
                        
                        st.success("✅ Resume uploaded successfully! Your information has been auto-filled.")
                        st.info("💡 Click 'Build Resume For Free' above to start editing with your pre-filled data.")
                        
                        # Show preview of extracted data
                        with st.expander("📋 Preview Extracted Data"):
                            if parsed_data.get('full_name'):
                                st.write(f"**Name:** {parsed_data['full_name']}")
                            if parsed_data.get('email'):
                                st.write(f"**Email:** {parsed_data['email']}")
                            if parsed_data.get('phone'):
                                st.write(f"**Phone:** {parsed_data['phone']}")
                            if parsed_data.get('summary'):
                                st.write(f"**Summary:** {parsed_data['summary'][:200]}...")
                            if parsed_data.get('tech_skills'):
                                st.write(f"**Skills:** {parsed_data['tech_skills'][:200]}...")
                            if parsed_data.get('work_entries'):
                                st.write(f"**Work Experience:** {len(parsed_data['work_entries'])} positions found")
                            if parsed_data.get('education_entries'):
                                st.write(f"**Education:** {len(parsed_data['education_entries'])} entries found")
                    
                    except Exception as e:
                        st.error(f"❌ Error parsing resume: {str(e)}")
                        st.info("💡 Please try a different file format or build your resume from scratch.")
        
        st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown("### 🌟 Stand Out with AI-Powered Career Tools")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='dashboard-card'>
            <h3>🤖 AI Resume Writer</h3>
            <p>Optimize your resume for any job with our AI. Customize content for specific roles and stand out to recruiters.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='dashboard-card'>
            <h3>✉️ Cover Letter Builder</h3>
            <p>Create compelling cover letters in minutes with AI. Multiple templates and styles to choose from.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='dashboard-card'>
            <h3>📊 ATS Score Checker</h3>
            <p>Ensure your resume passes ATS screening. Get detailed compatibility scores and keyword recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='dashboard-card'>
            <h3>💼 Content Library</h3>
            <p>Access pre-written bullet points and examples across 15+ job roles. Build faster with proven content.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Get Your Standout Resume in 4 Easy Steps")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='info-box' style='text-align: center;'>
            <h2>🎨</h2>
            <h4>1. Choose Template</h4>
            <p>Start with professional ATS-friendly templates. Change anytime with one click!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-box' style='text-align: center;'>
            <h2>📝</h2>
            <h4>2. Fill Details</h4>
            <p>Upload existing resume or use pre-written examples. Build your power resume!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='info-box' style='text-align: center;'>
            <h2>✨</h2>
            <h4>3. Customize</h4>
            <p>Personalize with colors, fonts, and AI-generated content tailored to your profile!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='info-box' style='text-align: center;'>
            <h2>📥</h2>
            <h4>4. Download</h4>
            <p>Download in PDF, DOCX, or other formats. 100% free, no credit card needed!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ATS Optimization Best Practices
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🎯 ATS Optimization Checklist")
    st.caption("Follow these proven strategies to beat Applicant Tracking Systems")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='dashboard-card'>
            <h4>✅ Do's for ATS Success</h4>
            <ul style='line-height: 1.8;'>
                <li><b>Use Keywords</b> from job descriptions (exact matches matter)</li>
                <li><b>Quantify Everything</b>: "Increased sales by 40%" not "Increased sales"</li>
                <li><b>Clean Format</b>: Simple layout, standard fonts (Arial, Calibri)</li>
                <li><b>Standard Sections</b>: Summary, Experience, Education, Skills</li>
                <li><b>Action Verbs</b>: Led, Built, Improved, Reduced, Increased</li>
                <li><b>Save as PDF</b> (or DOCX if specifically requested)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='dashboard-card'>
            <h4>❌ Don'ts That Hurt ATS Scores</h4>
            <ul style='line-height: 1.8;'>
                <li><b>NO Photos</b>: Confuses ATS, introduces bias (except Germany/France)</li>
                <li><b>NO Graphics/Icons</b>: ATS can't read images or charts</li>
                <li><b>NO Tables</b>: Most ATS struggle with table parsing</li>
                <li><b>NO Headers/Footers</b>: Content may not be read by ATS</li>
                <li><b>NO Fancy Fonts</b>: Stick to Arial, Calibri, Times New Roman</li>
                <li><b>NO Creative Layouts</b>: Two columns can confuse ATS</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer with secondary auth links
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    footer_col1, footer_col2, footer_col3, footer_col4 = st.columns([1, 1, 1, 1])
    
    with footer_col1:
        st.markdown("<p style='font-size: 0.85rem; color: #666;'>© 2026 SoulSkill. All rights reserved.</p>", unsafe_allow_html=True)
    
    with footer_col2:
        if st.button("About", use_container_width=True, key="footer_about", type="secondary"):
            st.session_state.mode = 'about'
            st.rerun()
    
    with footer_col3:
        if st.button("Contact", use_container_width=True, key="footer_contact", type="secondary"):
            st.session_state.mode = 'contact'
            st.rerun()
    
    with footer_col4:
        if not st.session_state.user_authenticated:
            if st.button("Sign In", use_container_width=True, key="footer_signin", type="secondary"):
                st.session_state.show_auth_modal = True
                st.rerun()
        else:
            st.markdown("<p style='font-size: 0.85rem; color: #2563eb;'>👤 Welcome!</p>", unsafe_allow_html=True)

elif st.session_state.mode == 'dashboard':
    # Resume Dashboard - Manage Multiple Resumes
    st.title("📂 My Resumes Dashboard")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Manage all your resumes in one place")
    with col2:
        if st.button("➕ Create New Resume", use_container_width=True):
            st.session_state.mode = 'builder'
            st.session_state.step = 1
            st.session_state.current_resume_id = None
            st.rerun()
    
    # Load saved resumes
    saved_resumes = st.session_state.get('resumes', {})
    
    if not saved_resumes:
        st.markdown("""
        <div class='info-box' style='text-align: center; padding: 3rem;'>
            <h2>📝</h2>
            <h3>No resumes yet</h3>
            <p>Create your first resume and manage multiple versions here!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display resumes as cards
        for resume_id, resume_data in saved_resumes.items():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                st.markdown(f"""
                <div class='card-header'>
                    <div>
                        <div class='card-title'>{resume_data.get('full_name', 'Untitled Resume')}</div>
                        <div style='color: #666; font-size: 0.9rem;'>{resume_data.get('job_title_target', 'No job title')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                completeness = resume_data.get('completeness', 0)
                st.metric("Completeness", f"{completeness}%")
            
            with col3:
                created_date = resume_data.get('created_at', 'Unknown')
                st.caption(f"Created: {created_date}")
            
            with col4:
                if st.button("✏️ Edit", key=f"edit_{resume_id}", use_container_width=True):
                    # Load resume data into session state
                    for key, value in resume_data.items():
                        st.session_state[key] = value
                    st.session_state.current_resume_id = resume_id
                    st.session_state.mode = 'builder'
                    st.session_state.step = 2
                    st.rerun()
            
            st.markdown("---")
    
    if st.button("🏠 Back to Home"):
        st.session_state.mode = 'home'
        st.rerun()

elif st.session_state.mode == 'builder':
    # Resume Builder - 4 Step Process
    render_step_indicator(st.session_state.step)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.step == 1:
        # STEP 1: Choose Template
        st.title("🎨 Choose Your Template")
        st.markdown("### Start strong with professional ATS-friendly templates")
        
        # Country and Category filters
        col1, col2 = st.columns(2)
        with col1:
            country_filter = st.selectbox(
                "🌍 Filter by Country/Region",
                ["All Countries", "India 🇮🇳", "USA 🇺🇸", "UK 🇬🇧", "Canada 🇨🇦", 
                 "Australia 🇦🇺", "Germany 🇩🇪", "France 🇫🇷", "UAE 🇦🇪", "Singapore 🇸🇬"],
                key="country_filter"
            )
        with col2:
            template_category = st.selectbox(
                "🎯 Filter by category",
                ["All Templates", "Professional", "Creative", "Tech", "Healthcare", "Business", "Education"],
                key="template_category_filter"
            )
        
        st.markdown("---")
        st.caption("💡 Click any template to see full preview, then select to use it")
        
        # Combine templates based on country filter
        all_templates = {**TEMPLATES}
        
        if country_filter == "All Countries":
            all_templates.update({**INDIAN_TEMPLATES, **US_TEMPLATES, **UK_TEMPLATES, 
                                **CANADA_TEMPLATES, **AUSTRALIA_TEMPLATES, **GERMANY_TEMPLATES,
                                **FRANCE_TEMPLATES, **UAE_TEMPLATES, **SINGAPORE_TEMPLATES})
        elif country_filter == "India 🇮🇳":
            all_templates.update({**INDIAN_TEMPLATES})
        elif country_filter == "USA 🇺🇸":
            all_templates.update({**US_TEMPLATES})
        elif country_filter == "UK 🇬🇧":
            all_templates.update({**UK_TEMPLATES})
        elif country_filter == "Canada 🇨🇦":
            all_templates.update({**CANADA_TEMPLATES})
        elif country_filter == "Australia 🇦🇺":
            all_templates.update({**AUSTRALIA_TEMPLATES})
        elif country_filter == "Germany 🇩🇪":
            all_templates.update({**GERMANY_TEMPLATES})
        elif country_filter == "France 🇫🇷":
            all_templates.update({**FRANCE_TEMPLATES})
        elif country_filter == "UAE 🇦🇪":
            all_templates.update({**UAE_TEMPLATES})
        elif country_filter == "Singapore 🇸🇬":
            all_templates.update({**SINGAPORE_TEMPLATES})
        
        # Display templates in grid with previews
        templates_list = list(all_templates.items())
        
        cols_per_row = 3
        for i in range(0, len(templates_list), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, (template_id, template_config) in enumerate(templates_list[i:i+cols_per_row]):
                with cols[j]:
                    selected = st.session_state.get('selected_template') == template_id
                    card_class = "selected" if selected else ""
                    
                    # Safe access to template properties with defaults
                    template_name = template_config.get('name', template_id.replace('_', ' ').title())
                    template_icon = template_config.get('icon', '📄')
                    template_desc = template_config.get('description', 'Professional template')
                    template_ats = template_config.get('ats_score', 90)
                    
                    # Generate preview HTML
                    preview_html = get_template_preview_html(template_config, template_id)
                    
                    # Show template name and description
                    st.markdown(f"""
                    <div style='text-align: center; margin-bottom: 0.5rem;'>
                        <div style='font-weight: bold; font-size: 0.95rem; margin-bottom: 0.25rem;'>{template_name}</div>
                        <div style='font-size: 0.75rem; color: #666; margin-bottom: 0.25rem;'>{template_desc}</div>
                        <div style='display: inline-block; background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600;'>{template_ats}% ATS</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Render actual preview in iframe
                    components.html(preview_html, height=240, scrolling=False)
                    
                    # Button with unique key and immediate action
                    button_key = f"template_select_{i}_{j}_{template_id}"
                    button_label = '✓ Selected' if selected else 'Select This Template'
                    if st.button(button_label, 
                               key=button_key, 
                               use_container_width=True,
                               disabled=selected,
                               type="primary" if selected else "secondary"):
                        st.session_state['selected_template'] = template_id
                        st.session_state['template'] = template_id
                        st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("🏠 Home"):
                st.session_state.mode = 'home'
                st.rerun()
        with col3:
            if st.session_state.get('selected_template'):
                if st.button("Next: Fill Details ➡️", use_container_width=True):
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.info("👆 Please select a template to continue")
    
    elif st.session_state.step == 2:
        # STEP 2: Fill Details (with content suggestions and resume upload)
        col_main, col_preview = st.columns([2, 1])
        
        with col_main:
            st.title("📝 Fill in Your Details")
            
            # Soulful affirmation
            affirmations = [
                "🌟 Your unique experiences make you valuable—let's showcase them!",
                "💪 Every achievement you list is proof of your growth and resilience.",
                "✨ You've already done the hard work—now let's tell your story.",
                "🎯 Your skills and passion will shine through this resume.",
                "🚀 Remember: You're not just listing jobs, you're sharing your journey."
            ]
            import random
            st.info(random.choice(affirmations))
            
            # Job Description Matcher - NEW FEATURE
            with st.expander("🎯 Paste Job Description (AI-Powered Keyword Matcher)", expanded=False):
                st.markdown("""
                **Tailor your resume for this specific job!** 
                Paste the job description below and we'll:
                - Extract key requirements and skills
                - Highlight what you already have
                - Suggest what's missing from your resume
                - Recommend keywords to include
                """)
                
                job_description = st.text_area(
                    "Job Description", 
                    height=200,
                    placeholder="Paste the full job description here...",
                    key="job_description_input",
                    help="Copy-paste from job posting for personalized optimization"
                )
                st.session_state.job_description = job_description
                
                if job_description and st.button("🔍 Analyze Job Match", key="analyze_jd_btn"):
                    with st.spinner("🤖 AI is analyzing job requirements..."):
                        if ai_assistant.enabled:
                            try:
                                # Extract keywords from JD
                                jd_analysis = ai_assistant.gemini_model.generate_content(
                                    f"""Analyze this job description and extract:
                                    1. Required technical skills (comma-separated)
                                    2. Required soft skills (comma-separated)
                                    3. Key responsibilities/requirements (bullet points)
                                    4. Keywords that should appear in resume (comma-separated)
                                    
                                    Format as:
                                    TECHNICAL_SKILLS: skill1, skill2, skill3
                                    SOFT_SKILLS: skill1, skill2, skill3
                                    REQUIREMENTS:
                                    - requirement 1
                                    - requirement 2
                                    KEYWORDS: keyword1, keyword2, keyword3
                                    
                                    Job Description:
                                    {job_description}"""
                                )
                                
                                analysis_text = jd_analysis.text
                                st.session_state.jd_analysis = analysis_text
                                
                                # Parse analysis
                                tech_skills_match = []
                                soft_skills_match = []
                                keywords_match = []
                                
                                if 'TECHNICAL_SKILLS:' in analysis_text:
                                    tech_line = analysis_text.split('TECHNICAL_SKILLS:')[1].split('SOFT_SKILLS:')[0].strip()
                                    jd_tech_skills = [s.strip() for s in tech_line.split(',')]
                                    user_tech_skills = st.session_state.get('tech_skills', '').lower()
                                    tech_skills_match = [s for s in jd_tech_skills if s.lower() in user_tech_skills]
                                
                                st.success("✅ Job analysis complete!")
                                
                                # Show results
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown("**✅ Skills You Have:**")
                                    if tech_skills_match:
                                        for skill in tech_skills_match:
                                            st.markdown(f"- {skill}")
                                    else:
                                        st.caption("Add your skills below to see matches")
                                
                                with col2:
                                    st.markdown("**⚠️ Missing Skills to Add:**")
                                    if 'TECHNICAL_SKILLS:' in analysis_text:
                                        missing = [s for s in jd_tech_skills if s not in tech_skills_match]
                                        for skill in missing[:5]:
                                            st.markdown(f"- {skill}")
                                
                                # Store for later reference
                                st.session_state.jd_tech_skills = jd_tech_skills if 'TECHNICAL_SKILLS:' in analysis_text else []
                                
                            except Exception as e:
                                st.error(f"Analysis failed: {str(e)}")
                        else:
                            st.warning("AI features require Google API key in secrets.toml")
            
            # Option to upload existing resume
            with st.expander("📤 Upload Existing Resume (Auto-fill)", expanded=False):
                uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'], key="resume_upload_step2")
                if uploaded_file and st.button("🤖 Extract & Auto-Fill", key="extract_btn_step2"):
                    with st.spinner("Extracting information from your resume..."):
                        try:
                            importer = ResumeImporter()
                            if uploaded_file.type == "application/pdf":
                                extracted = importer.parse_pdf(uploaded_file)
                            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                                extracted = importer.parse_docx(uploaded_file)
                            else:
                                extracted = importer.parse_text(uploaded_file.read().decode('utf-8'))
                            
                            # Auto-fill fields
                            if extracted:
                                for key, value in extracted.items():
                                    if value:
                                        st.session_state[key] = value
                                st.success("✅ Resume information extracted! Fields auto-filled.")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error extracting resume: {str(e)}")
            
            # Personal Information
            st.markdown("### 👤 Personal Information")
            
            # LinkedIn Profile Alignment Tip
            if not st.session_state.get('linkedin'):
                st.warning("💡 **Pro Tip**: Add your LinkedIn URL! Recruiters check LinkedIn profiles 80% of the time. Ensure your LinkedIn matches your resume for consistency.")
            
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *", value=st.session_state.get('full_name', ''), key="fname_step2")
                email = st.text_input("Email *", value=st.session_state.get('email', ''), key="email_step2")
                phone = st.text_input("Phone *", value=st.session_state.get('phone', ''), key="phone_step2")
            with col2:
                # Autocomplete for city
                datalist_html_city = '<datalist id="cities">' + ''.join([f'<option value="{c}">' for c in CITIES]) + '</datalist>'
                st.markdown(datalist_html_city, unsafe_allow_html=True)
                
                city_value = st.session_state.get('city', '')
                city = st.text_input("City *", value=city_value, 
                                    placeholder="Type city name...",
                                    key="city_step2",
                                    help="Start typing to see suggestions")
                
                linkedin = st.text_input("LinkedIn URL", value=st.session_state.get('linkedin', ''), 
                                        key="linkedin_step2",
                                        help="Ensure your LinkedIn headline and summary match your resume!")
                portfolio = st.text_input("Portfolio/Website", value=st.session_state.get('portfolio', ''), key="portfolio_step2")
            
            # LinkedIn alignment checker
            if linkedin and st.session_state.get('summary'):
                st.success("✅ **LinkedIn Sync**: Make sure your LinkedIn 'About' section echoes your professional summary above for consistency!")
            
            # Update session state
            st.session_state.full_name = full_name
            st.session_state.email = email
            st.session_state.phone = phone
            st.session_state.city = city
            st.session_state.linkedin = linkedin
            st.session_state.portfolio = portfolio
            
            # Job Target
            st.markdown("### 🎯 Job Target")
            col1, col2 = st.columns(2)
            with col1:
                # Autocomplete for job title
                datalist_html = '<datalist id="jobtitles">' + ''.join([f'<option value="{title}">' for title in JOB_TITLES]) + '</datalist>'
                st.markdown(datalist_html, unsafe_allow_html=True)
                
                job_title_value = st.session_state.get('job_title_target', '')
                job_title = st.text_input("Target Job Title *", value=job_title_value, 
                                         placeholder="e.g., Software Engineer (Type for suggestions...)", 
                                         key="jobtitle_step2")
                
                # Show popular suggestions
                if not job_title_value:
                    with st.expander("💡 Popular Job Titles", expanded=False):
                        cols = st.columns(3)
                        for idx, title in enumerate(JOB_TITLES[:12]):
                            with cols[idx % 3]:
                                if st.button(title, key=f"jobtitle_suggest_{idx}", use_container_width=True):
                                    st.session_state.job_title_target = title
                                    st.rerun()
                
                st.session_state.job_title_target = job_title
            with col2:
                ind_idx = 0
                if st.session_state.get('industry') in INDUSTRY_OPTIONS:
                    ind_idx = INDUSTRY_OPTIONS.index(st.session_state.get('industry')) + 1
                industry = st.selectbox("Industry *", options=[""] + INDUSTRY_OPTIONS, index=ind_idx, key="industry_step2")
                st.session_state.industry = industry
            
            # Professional Summary with AI and Examples
            st.markdown("### 📝 Professional Summary")
            
            # Get content suggestions based on job title
            selected_role = job_title if job_title else "Software Engineer"
            suggestions = get_content_suggestions(selected_role, "summaries")
            
            if suggestions and st.checkbox("💡 Show Pre-written Examples", key="show_summary_examples"):
                st.markdown("<div class='info-box'>Click any example to use it as your summary:</div>", unsafe_allow_html=True)
                for idx, suggestion in enumerate(suggestions):
                    if st.button(f"📋 Use Example {idx+1}", key=f"summary_suggestion_{idx}", use_container_width=False):
                        st.session_state.summary = suggestion
                        st.rerun()
                    st.markdown(f"<div class='content-suggestion'><div class='suggestion-text'>{suggestion}</div></div>", unsafe_allow_html=True)
            
            summary = st.text_area("Professional Summary *", value=st.session_state.get('summary', ''), 
                                  height=150, placeholder="Write a compelling summary of your professional background...",
                                  key="summary_step2",
                                  on_change=lambda: auto_save_field('summary', st.session_state.summary_step2))
            if summary != st.session_state.get('summary', ''):
                st.session_state.summary = summary
                st.caption("💾 Auto-saved")
            
            if ai_assistant.enabled:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✨ Generate with AI", key="ai_summary_btn", use_container_width=True):
                        with st.spinner("Generating AI summary..."):
                            profile_data = {
                                'job_title_target': job_title,
                                'industry': industry,
                                'tech_skills': st.session_state.get('tech_skills', ''),
                                'soft_skills': st.session_state.get('soft_skills', ''),
                                'profile_type': 'experienced' if st.session_state.get('work_entries') else 'fresher',
                                'full_name': st.session_state.get('full_name', '')
                            }
                            ai_summary = ai_assistant.generate_professional_summary(profile_data)
                            if ai_summary:
                                st.session_state.summary = ai_summary
                                st.rerun()
            
            # Skills
            st.markdown("### 💪 Skills")
            
            # Get skill suggestions
            skill_suggestions = get_content_suggestions(selected_role, "skills")
            if skill_suggestions:
                st.markdown("**💡 Suggested Skills:**")
                skill_cols = st.columns(4)
                for idx, skill in enumerate(skill_suggestions[:12]):
                    with skill_cols[idx % 4]:
                        if st.button(f"➕ {skill}", key=f"skill_suggest_{idx}", use_container_width=True):
                            current_skills = st.session_state.get('tech_skills', '')
                            if current_skills:
                                st.session_state.tech_skills = current_skills + ", " + skill
                            else:
                                st.session_state.tech_skills = skill
                            st.rerun()
            
            # Autocomplete for skills
            skill_datalist_html = '<datalist id="techskills">' + ''.join([f'<option value="{skill}">' for skill in TECHNICAL_SKILLS]) + '</datalist>'
            st.markdown(skill_datalist_html, unsafe_allow_html=True)
            
            tech_skills = st.text_area("Technical Skills *", value=st.session_state.get('tech_skills', ''), 
                                      placeholder="Start typing skill names... (e.g., Python, JavaScript, React)",
                                      key="techskills_step2",
                                      help="Type to see autocomplete suggestions. Separate skills with commas.",
                                      height=100)
            if tech_skills != st.session_state.get('tech_skills', ''):
                st.session_state.tech_skills = tech_skills
            
            soft_skills = st.text_area("Soft Skills", value=st.session_state.get('soft_skills', ''), 
                                      placeholder="Leadership, Communication, Problem Solving...", key="softskills_step2")
            if soft_skills != st.session_state.get('soft_skills', ''):
                st.session_state.soft_skills = soft_skills
            
            # Skill Gap Analysis - show if JD was analyzed
            if st.session_state.get('jd_tech_skills'):
                jd_skills = st.session_state.jd_tech_skills
                user_skills_lower = tech_skills.lower()
                
                matching_skills = [s for s in jd_skills if s.lower() in user_skills_lower]
                missing_skills = [s for s in jd_skills if s.lower() not in user_skills_lower]
                
                match_percentage = (len(matching_skills) / len(jd_skills) * 100) if jd_skills else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Match Score", f"{match_percentage:.0f}%", 
                             help="How well your skills match the job requirements")
                with col2:
                    st.metric("Matched Skills", len(matching_skills))
                with col3:
                    st.metric("Missing Skills", len(missing_skills))
                
                if missing_skills and match_percentage < 70:
                    st.warning(f"⚠️ **Skill Gap Alert**: Consider adding these skills if you have them: {', '.join(missing_skills[:5])}")
                elif match_percentage >= 70:
                    st.success(f"🌟 **Great match!** Your skills align well with the job. Keep highlighting these in your work experience!")
            
            # Auto-save indicator
            if tech_skills or soft_skills:
                st.caption("💾 Changes saved automatically")
            
            # Work Experience
            st.markdown("### 💼 Work Experience")
            
            # Show quantification tips for tech/business roles
            job_title = st.session_state.get('job_title_target', '').lower()
            quantifiable_roles = ['engineer', 'developer', 'manager', 'analyst', 'data', 'product', 'sales', 'marketing', 'project']
            
            if any(role in job_title for role in quantifiable_roles):
                st.info("💡 **Pro Tip**: Quantify your achievements! Examples:\n"
                       "- ✅ 'Improved app performance by 30%' vs ❌ 'Improved performance'\n"
                       "- ✅ 'Led team of 5 developers' vs ❌ 'Led a team'\n"
                       "- ✅ 'Reduced costs by $50K annually' vs ❌ 'Saved money'\n"
                       "- ✅ 'Increased user engagement by 40%' vs ❌ 'Improved engagement'")
            
            if 'work_entries' not in st.session_state:
                st.session_state.work_entries = []
            
            # Show existing entries
            for idx, entry in enumerate(st.session_state.work_entries):
                with st.expander(f"📌 {entry.get('title', 'Position')} at {entry.get('company', 'Company')}", expanded=False):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{entry.get('title')}** | {entry.get('company')}")
                        st.caption(f"{entry.get('start_date')} - {entry.get('end_date')}")
                    with col2:
                        if st.button("🗑️ Remove", key=f"remove_work_{idx}"):
                            st.session_state.work_entries.pop(idx)
                            st.rerun()
            
            # Add new work experience
            with st.expander("➕ Add Work Experience", expanded=len(st.session_state.work_entries) == 0):
                # Autocomplete for job title in work experience
                datalist_work = '<datalist id="worktitles">' + ''.join([f'<option value="{title}">' for title in JOB_TITLES]) + '</datalist>'
                st.markdown(datalist_work, unsafe_allow_html=True)
                
                work_title = st.text_input("Job Title", key="new_work_title", 
                                          placeholder="Type to see suggestions...")
                
                # Autocomplete for company
                datalist_company = '<datalist id="companies">' + ''.join([f'<option value="{comp}">' for comp in COMPANIES]) + '</datalist>'
                st.markdown(datalist_company, unsafe_allow_html=True)
                
                work_company = st.text_input("Company", key="new_work_company",
                                            placeholder="Type company name...")
                col1, col2 = st.columns(2)
                with col1:
                    work_start = st.text_input("Start Date", placeholder="Jan 2020", key="new_work_start")
                with col2:
                    work_end = st.text_input("End Date", placeholder="Present", key="new_work_end")
                
                # Show work bullet suggestions
                work_bullets = get_content_suggestions(selected_role, "work_bullets")
                if work_bullets and st.checkbox("💡 Show Example Bullet Points", key="show_work_bullets"):
                    st.markdown("<div class='info-box'>Click to add any bullet point:</div>", unsafe_allow_html=True)
                    for b_idx, bullet in enumerate(work_bullets[:6]):
                        if st.button(f"➕ Add: {bullet[:60]}...", key=f"work_bullet_{b_idx}"):
                            current_resp = st.session_state.get('new_work_resp', '')
                            if current_resp:
                                st.session_state.new_work_resp = current_resp + "\n• " + bullet
                            else:
                                st.session_state.new_work_resp = "• " + bullet
                            st.rerun()
                
                work_resp = st.text_area("Responsibilities & Achievements", 
                                        value=st.session_state.get('new_work_resp', ''),
                                        height=120, placeholder="• Achieved...\n• Developed...\n• Led...",
                                        key="new_work_resp",
                                        help="🌟 Remember: Every task you completed showed dedication. Focus on the impact you made!")
                
                # Guided suggestions box
                if work_resp and len(work_resp) < 50:
                    st.warning("💡 **Enrich Your Content**: Add measurable achievements! Example: 'Led migration of 10+ microservices reducing latency by 40%'")
                elif work_resp and not any(char.isdigit() for char in work_resp):
                    st.info("💪 **Add Numbers**: Quantify your impact! Include metrics like percentages, dollar amounts, team sizes, or timeframes.")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✅ Add Work Experience", key="add_work_btn", use_container_width=True):
                        if work_title and work_company:
                            st.session_state.work_entries.append({
                                'title': work_title,
                                'company': work_company,
                                'start_date': work_start,
                                'end_date': work_end,
                                'responsibilities': work_resp
                            })
                            # Affirmation on save
                            st.balloons()
                            st.success("🌟 Great! You're building a powerful story of your professional journey!")
                            # Clear fields
                            st.session_state.new_work_resp = ''
                            st.success("✅ Work experience added!")
                            st.rerun()
                        else:
                            st.warning("Please fill in Job Title and Company")
                
                with col_btn2:
                    if st.button("💾 Save Draft", key="save_work_draft", use_container_width=True):
                        st.info("Draft saved! Fill remaining fields to add.")
            
            # Education
            st.markdown("### 🎓 Education")
            
            if 'education_entries' not in st.session_state:
                st.session_state.education_entries = []
            
            # Show existing entries
            for idx, entry in enumerate(st.session_state.education_entries):
                with st.expander(f"🎓 {entry.get('degree', 'Degree')} - {entry.get('institution', 'Institution')}", expanded=False):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{entry.get('degree')}** in {entry.get('stream')}")
                        st.caption(f"{entry.get('institution')} | {entry.get('year')}")
                    with col2:
                        if st.button("🗑️ Remove", key=f"remove_edu_{idx}"):
                            st.session_state.education_entries.pop(idx)
                            st.rerun()
            
            # Add new education
            with st.expander("➕ Add Education", expanded=len(st.session_state.education_entries) == 0):
                edu_degree = st.selectbox("Degree", options=DEGREE_OPTIONS, key="new_edu_degree")
                edu_stream = st.text_input("Field of Study", key="new_edu_stream")
                edu_institution = st.text_input("Institution", key="new_edu_institution")
                col1, col2 = st.columns(2)
                with col1:
                    edu_year = st.text_input("Graduation Year", placeholder="2020", key="new_edu_year")
                with col2:
                    edu_score = st.text_input("GPA/Percentage", placeholder="8.5 CGPA", key="new_edu_score")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✅ Add Education", key="add_edu_btn", use_container_width=True):
                        if edu_degree and edu_institution:
                            st.session_state.education_entries.append({
                                'degree': edu_degree,
                                'stream': edu_stream,
                                'institution': edu_institution,
                                'year': edu_year,
                                'score': edu_score
                            })
                            st.success("✅ Education added!")
                            st.rerun()
                        else:
                            st.warning("Please fill in Degree and Institution")
                
                with col_btn2:
                    if st.button("💾 Save Draft", key="save_edu_draft", use_container_width=True):
                        st.info("Draft saved! Fill remaining fields to add.")
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        with col_preview:
            st.markdown("### 👁️ Live Preview")
            completeness = calculate_completeness()
            st.progress(completeness / 100)
            st.caption(f"Resume Completeness: {completeness}%")
            
            if st.session_state.get('full_name'):
                st.markdown(f"**{st.session_state.get('full_name')}**")
                st.caption(st.session_state.get('job_title_target', 'Job Title'))
                st.caption(f"📧 {st.session_state.get('email', '')}")
                st.caption(f"📱 {st.session_state.get('phone', '')}")
            
            if st.session_state.get('work_entries'):
                st.markdown(f"**💼 Experience:** {len(st.session_state.work_entries)} positions")
            
            if st.session_state.get('education_entries'):
                st.markdown(f"**🎓 Education:** {len(st.session_state.education_entries)} entries")
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Templates", key="back_from_step2", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("Next: Customize ➡️", key="next_from_step2", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
    
    elif st.session_state.step == 3:
        # STEP 3: Customize (Colors, Fonts, AI Content, Template Switch)
        col_main, col_preview = st.columns([1, 1])
        
        with col_main:
            st.title("✨ Customize Your Resume")
            
            # Role-specific tips based on job title
            job_title = st.session_state.get('job_title_target', '').lower()
            tech_roles = ['software', 'developer', 'engineer', 'data', 'ai', 'ml', 'devops', 'tech', 'programmer', 'genai', 'product']
            
            if any(role in job_title for role in tech_roles):
                st.info("""
                **💡 Tech Role Resume Tips:**
                
                ✅ **ATS-Optimized**: Use keywords from job descriptions (e.g., Python, React, AWS, Agile)
                
                ✅ **Quantify Achievements**: "Improved app performance by 30%" not just "Improved performance"
                
                ✅ **Clean Format**: No photos, graphics, or fancy designs - keep it simple for ATS parsing
                
                ✅ **Show Impact**: Focus on metrics and business outcomes (user growth, cost savings, efficiency gains)
                
                💼 **Showcase Personality Elsewhere**: Use LinkedIn profile and personal website/portfolio for visual presence
                """)
            
            # Template Switcher
            st.markdown("### 🎨 Change Template")
            st.caption("Switch templates anytime with one click!")
            
            all_templates = {**TEMPLATES, **INDIAN_TEMPLATES, **US_TEMPLATES, **UK_TEMPLATES, 
                           **CANADA_TEMPLATES, **AUSTRALIA_TEMPLATES, **GERMANY_TEMPLATES,
                           **FRANCE_TEMPLATES, **UAE_TEMPLATES, **SINGAPORE_TEMPLATES}
            current_template = st.session_state.get('selected_template', list(all_templates.keys())[0])
            
            template_cols = st.columns(4)
            for idx, (template_id, template_config) in enumerate(list(all_templates.items())[:8]):
                with template_cols[idx % 4]:
                    is_selected = current_template == template_id
                    button_label = f"{'✓ ' if is_selected else ''}{template_config.get('icon', '📄')}"
                    if st.button(button_label, key=f"template_switch_{template_id}", use_container_width=True):
                        st.session_state.selected_template = template_id
                        st.session_state.template = template_id
                        st.rerun()
                    template_name = template_config.get('name', template_id.replace('_', ' ').title())
                    st.caption(template_name[:12])
            
            st.markdown("---")
            
            # Color Theme Picker
            st.markdown("### 🎨 Color Theme")
            
            color_themes = {
                'blue': {'primary': '#667eea', 'secondary': '#764ba2', 'name': 'Professional Blue'},
                'green': {'primary': '#11998e', 'secondary': '#38ef7d', 'name': 'Success Green'},
                'purple': {'primary': '#a8c0ff', 'secondary': '#3f2b96', 'name': 'Royal Purple'},
                'orange': {'primary': '#f093fb', 'secondary': '#f5576c', 'name': 'Creative Orange'},
                'navy': {'primary': '#2c3e50', 'secondary': '#3498db', 'name': 'Corporate Navy'},
                'red': {'primary': '#fc4a1a', 'secondary': '#f7b733', 'name': 'Bold Red'}
            }
            
            color_cols = st.columns(6)
            for idx, (theme_id, theme_data) in enumerate(color_themes.items()):
                with color_cols[idx]:
                    is_selected = st.session_state.get('color_theme', 'blue') == theme_id
                    if st.button(f"{'✓' if is_selected else '●'}", key=f"color_{theme_id}", use_container_width=True,
                                help=theme_data['name']):
                        st.session_state.color_theme = theme_id
                        st.rerun()
                    st.markdown(f"<div style='background: linear-gradient(135deg, {theme_data['primary']}, {theme_data['secondary']}); height: 30px; border-radius: 8px; margin-bottom: 5px;'></div>", unsafe_allow_html=True)
                    st.caption(theme_data['name'].split()[0])
            
            st.markdown("---")
            
            # Font Family
            st.markdown("### 🔤 Font Style")
            
            fonts = {
                'Arial': 'Clean & Professional',
                'Helvetica': 'Modern & Minimal',
                'Georgia': 'Classic & Elegant',
                'Times New Roman': 'Traditional & Formal',
                'Calibri': 'Friendly & Readable',
                'Verdana': 'Clear & Bold'
            }
            
            font_cols = st.columns(3)
            for idx, (font_name, font_desc) in enumerate(fonts.items()):
                with font_cols[idx % 3]:
                    is_selected = st.session_state.get('font_family', 'Arial') == font_name
                    if st.button(f"{'✓ ' if is_selected else ''}{font_name}", key=f"font_{font_name}", use_container_width=True):
                        st.session_state.font_family = font_name
                        st.rerun()
                    st.caption(font_desc)
            
            st.markdown("---")
            
            # Additional Options
            st.markdown("### ⚙️ Additional Options")
            
            col1, col2 = st.columns(2)
            with col1:
                # Photo option with regional guidance
                selected_template = st.session_state.get('selected_template', '')
                
                # Determine region based on template
                photo_required_regions = ['German Lebenslauf', 'French CV', 'Paris Creative']
                photo_discouraged_regions = ['Professional Blue', 'Harvard Business', 'Silicon Valley Tech', 
                                             'British Standard', 'Canadian Professional', 'Aussie Standard']
                
                if selected_template in photo_required_regions:
                    photo_help = "✅ Photos are commonly expected for CVs in Germany/France"
                elif selected_template in photo_discouraged_regions:
                    photo_help = "⚠️ NOT recommended - Photos reduce ATS compatibility and may cause bias (India/US/UK/Australia standard)"
                else:
                    photo_help = "⚠️ Generally discouraged - Photos can confuse ATS and introduce unconscious bias"
                
                show_photo = st.checkbox("Include Photo", 
                                        value=st.session_state.get('show_photo', False), 
                                        key="show_photo_opt",
                                        help=photo_help)
                st.session_state.show_photo = show_photo
                
                if show_photo:
                    # Show detailed tips when photo is enabled
                    st.warning("⚠️ **Photo Added - Important Tips:**")
                    
                    with st.expander("📸 **Professional Photo Guidelines** (Click to expand)", expanded=True):
                        st.markdown("""
                        **✅ DO:**
                        - Use a **professional headshot** with good lighting
                        - **Plain background** (solid color, preferably neutral)
                        - **Business attire** appropriate for your industry
                        - **Recent photo** (taken within last 6 months)
                        - **High resolution** (at least 300 DPI for print)
                        - **Proper framing**: Head and shoulders, facing camera
                        - **Neutral expression**: Friendly, confident smile
                        - **Passport-size dimensions** if required (Germany/France: 2x2 inches)
                        
                        **❌ DON'T:**
                        - Selfies or casual photos
                        - Sunglasses, hats, or distracting accessories
                        - Group photos or cropped party pictures
                        - Filters, heavy editing, or old photos
                        - Dark, blurry, or low-quality images
                        - Inappropriate backgrounds (bedroom, bathroom, vacation)
                        - Full body shots or posed fashion photos
                        
                        **⚠️ ATS Warning:**
                        - **75% of resumes** with photos are auto-rejected by ATS in US/UK/India
                        - Photos can **confuse parsing algorithms** and cause formatting errors
                        - May introduce **unconscious bias** based on appearance, age, gender, or ethnicity
                        
                        **💡 Better Alternative:**
                        - Keep your resume photo-free for maximum ATS compatibility
                        - Use a **professional LinkedIn profile picture** instead
                        - Recruiters check LinkedIn anyway - this keeps your resume clean and ATS-friendly
                        - Add your LinkedIn URL to the contact section for easy access
                        
                        **🌍 Regional Guidelines:**
                        - **🇮🇳 India**: Photos strongly discouraged (ATS standard)
                        - **🇺🇸 USA**: Almost never include photos (illegal to request)
                        - **🇬🇧 UK**: Photos discouraged (bias concerns)
                        - **🇨🇦 Canada**: Not recommended (similar to US)
                        - **🇦🇺 Australia**: Generally avoided (ATS standard)
                        - **🇩🇪 Germany**: Often expected (but becoming less common)
                        - **🇫🇷 France**: Sometimes included (but not mandatory)
                        - **🇸🇬 Singapore**: Depends on industry (conservative approach)
                        - **🇦🇪 UAE**: Mixed, but trending toward no photos
                        
                        **🎯 When Photos ARE Acceptable:**
                        - Acting, modeling, or entertainment industry
                        - Media, TV, or on-camera roles
                        - Countries where it's explicitly expected (Germany, France)
                        - Personal branding for entrepreneurs/influencers
                        - Creative portfolios alongside traditional resume
                        """)
                    
                    st.info("💡 **Recommendation**: Consider removing the photo for better ATS results, especially if applying in US, UK, India, Canada, or Australia.")
                
                show_icons = st.checkbox("Show Icons", value=st.session_state.get('show_icons', True), key="show_icons_opt")
                st.session_state.show_icons = show_icons
            
            with col2:
                compact_mode = st.checkbox("Compact Layout", value=st.session_state.get('compact_mode', False), key="compact_opt")
                st.session_state.compact_mode = compact_mode
                
                two_column = st.checkbox("Two-Column Layout", value=st.session_state.get('two_column', False), key="two_col_opt")
                st.session_state.two_column = two_column
            
            st.markdown("---")
            
            # ATS Best Practices Info
            with st.expander("📊 ATS Best Practices - Read This Before Adding Photo"):
                st.markdown("""
                **Why Photos Are Generally NOT Recommended:**
                
                ✅ **ATS Compatibility**: Most resumes are scanned by Applicant Tracking Systems (ATS). Photos can:
                - Confuse parsing algorithms
                - Reduce your resume's chances of being shortlisted
                - Cause formatting issues that make your resume unreadable
                
                ⚠️ **Bias & Discrimination Risks**: Photos may lead to unconscious bias based on:
                - Appearance, age, gender, or ethnicity
                - Keep focus on your skills and achievements, not appearance
                
                🌍 **Regional Norms:**
                - **🇮🇳 India, 🇺🇸 US, 🇬🇧 UK, 🇨🇦 Canada, 🇦🇺 Australia**: Photos are **discouraged**
                - **🇩🇪 Germany, 🇫🇷 France**: Sometimes expected, but still optional
                - **Creative Industries** (acting, modeling, media): Photos often required
                
                💡 **Professional Branding Alternative:**
                - Use a polished **LinkedIn profile picture** instead
                - Recruiters check LinkedIn anyway - keeps your resume clean and ATS-friendly
                - Add your LinkedIn URL to contact section
                """)
            
            st.markdown("---")
            
            # AI Enhancement
            if ai_assistant.enabled:
                st.markdown("### ✨ AI Enhancement")
                st.caption("Improve your resume content with AI")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🚀 Enhance All Content", key="ai_enhance_all", use_container_width=True):
                        with st.spinner("AI is enhancing your resume..."):
                            # Enhance summary
                            if st.session_state.get('summary'):
                                enhanced = ai_assistant.enhance_content(st.session_state.summary)
                                if enhanced:
                                    st.session_state.summary = enhanced
                            
                            # Enhance work entries
                            for entry in st.session_state.get('work_entries', []):
                                if entry.get('responsibilities'):
                                    enhanced = ai_assistant.enhance_content(entry['responsibilities'])
                                    if enhanced:
                                        entry['responsibilities'] = enhanced
                            
                            st.success("✅ Content enhanced with AI!")
                            st.rerun()
                
                with col2:
                    if st.button("🔍 Check Spelling", key="spell_check_btn", use_container_width=True):
                        checker = SpellChecker()
                        issues = []
                        
                        # Check summary
                        if st.session_state.get('summary'):
                            summary_issues = checker.check_text(st.session_state.summary)
                            issues.extend(summary_issues)
                        
                        if issues:
                            st.warning(f"Found {len(issues)} potential issues")
                            for issue in issues[:5]:
                                st.caption(f"• {issue}")
                        else:
                            st.success("✅ No spelling issues found!")
            
            st.markdown("---")
            
            # ATS Score Preview
            st.markdown("### 📊 ATS Compatibility")
            
            if st.button("🔍 Check ATS Score", key="ats_preview_btn", use_container_width=True):
                with st.spinner("Calculating ATS score..."):
                    # Generate resume HTML
                    all_templates = {**TEMPLATES, **INDIAN_TEMPLATES}
                    template_config = all_templates[st.session_state.get('selected_template', list(all_templates.keys())[0])]
                    resume_html = generate_resume_html(st.session_state, template_config)
                    
                    # Check format compatibility
                    format_check = ATSOptimizer.check_format_compatibility(resume_html)
                    
                    st.metric("ATS Compatibility Score", f"{format_check['score']}%")
                    
                    if format_check['score'] >= 80:
                        st.success("✅ Excellent! Your resume is highly ATS-compatible")
                    elif format_check['score'] >= 60:
                        st.warning("⚠️ Good, but could be improved")
                    else:
                        st.error("❌ Needs improvement for ATS systems")
                    
                    if format_check.get('recommendations'):
                        st.markdown("**Recommendations:**")
                        for rec in format_check['recommendations'][:3]:
                            st.caption(f"• {rec}")
        
        with col_preview:
            st.markdown("### 👁️ Live Preview")
            
            # Generate preview
            try:
                all_templates = {**TEMPLATES, **INDIAN_TEMPLATES}
                template_config = all_templates[st.session_state.get('selected_template', list(all_templates.keys())[0])]
                
                # Apply customizations to template
                if st.session_state.get('color_theme'):
                    theme = color_themes.get(st.session_state.color_theme, color_themes['blue'])
                    # Inject color theme into HTML (simplified)
                
                resume_html = generate_resume_html(st.session_state, template_config)
                
                # Show preview in iframe
                st.components.v1.html(resume_html, height=600, scrolling=True)
            except Exception as e:
                st.info("Preview will appear here")
                st.caption(f"Add more details in Step 2 to see preview")
        
        # Navigation
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Details", key="back_from_step3", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("Next: Download ➡️", key="next_from_step3", use_container_width=True):
                st.session_state.step = 4
                st.rerun()
    
    elif st.session_state.step == 4:
        # STEP 4: Download & Export with ATS Analysis
        st.title("📥 Download Your Resume")
        
        # Congratulatory affirmation
        st.success("🎉 **Congratulations!** You've completed your resume—a powerful reflection of your journey and achievements!")
        
        col_main, col_score = st.columns([2, 1])
        
        with col_main:
            # ATS Compatibility Checker - NEW FEATURE
            with st.expander("🔍 ATS Compatibility Check", expanded=True):
                st.markdown("### Ensuring Your Resume Passes ATS Screening")
                
                # Check for ATS issues
                ats_issues = []
                ats_warnings = []
                ats_pass = []
                
                # Check 1: Photo
                if st.session_state.get('show_photo'):
                    ats_issues.append("❌ **Photo included**: Remove photo for better ATS compatibility (except Germany/France)")
                else:
                    ats_pass.append("✅ No photo - ATS friendly")
                
                # Check 2: Complex formatting
                if st.session_state.get('two_column'):
                    ats_warnings.append("⚠️ **Two-column layout**: Some ATS may struggle with columns")
                else:
                    ats_pass.append("✅ Single column layout - ATS optimal")
                
                # Check 3: Content length
                total_content = len(st.session_state.get('summary', '') + st.session_state.get('tech_skills', ''))
                if total_content < 200:
                    ats_warnings.append("⚠️ **Thin content**: Add more keywords and details for better ATS matching")
                else:
                    ats_pass.append("✅ Sufficient content for keyword matching")
                
                # Check 4: Keywords presence
                if st.session_state.get('tech_skills') and len(st.session_state.get('tech_skills', '').split(',')) >= 5:
                    ats_pass.append("✅ Good number of technical skills listed")
                else:
                    ats_warnings.append("⚠️ **Limited skills**: Add more relevant skills for ATS keyword matching")
                
                # Check 5: Quantified achievements
                work_content = ' '.join([entry.get('responsibilities', '') for entry in st.session_state.get('work_entries', [])])
                has_numbers = any(char.isdigit() for char in work_content)
                if has_numbers:
                    ats_pass.append("✅ Achievements quantified with metrics")
                else:
                    ats_warnings.append("⚠️ **No metrics found**: Add numbers to strengthen impact (e.g., '30% improvement')")
                
                # Check 6: Standard sections
                required_sections = ['summary', 'tech_skills', 'work_entries']
                all_present = all(st.session_state.get(section) for section in required_sections)
                if all_present:
                    ats_pass.append("✅ All standard sections present")
                else:
                    ats_issues.append("❌ **Missing sections**: Ensure Summary, Skills, and Experience are filled")
                
                # Calculate ATS score
                total_checks = len(ats_pass) + len(ats_warnings) + len(ats_issues)
                ats_score = int((len(ats_pass) / total_checks * 100)) if total_checks > 0 else 0
                
                # Display score
                if ats_score >= 80:
                    st.success(f"### 🎯 ATS Score: {ats_score}%")
                    st.markdown("**Excellent!** Your resume is well-optimized for ATS systems.")
                elif ats_score >= 60:
                    st.warning(f"### ⚠️ ATS Score: {ats_score}%")
                    st.markdown("**Good**, but there's room for improvement.")
                else:
                    st.error(f"### ❌ ATS Score: {ats_score}%")
                    st.markdown("**Needs attention** - address issues below to improve.")
                
                # Show details
                col1, col2 = st.columns(2)
                with col1:
                    if ats_pass:
                        st.markdown("**✅ Strengths:**")
                        for item in ats_pass:
                            st.markdown(item)
                
                with col2:
                    if ats_warnings:
                        st.markdown("**⚠️ Warnings:**")
                        for item in ats_warnings:
                            st.markdown(item)
                    if ats_issues:
                        st.markdown("**❌ Issues:**")
                        for item in ats_issues:
                            st.markdown(item)
                
                st.info("💡 **Remember**: ATS systems look for keywords, clean formatting, and standard sections. Keep it simple!")
            
            # Generate final resume
            all_templates = {**TEMPLATES, **INDIAN_TEMPLATES, **US_TEMPLATES, **UK_TEMPLATES, 
                           **CANADA_TEMPLATES, **AUSTRALIA_TEMPLATES, **GERMANY_TEMPLATES,
                           **FRANCE_TEMPLATES, **UAE_TEMPLATES, **SINGAPORE_TEMPLATES}
            template_config = all_templates[st.session_state.get('selected_template', list(all_templates.keys())[0])]
            resume_html = generate_resume_html(st.session_state, template_config)
            
            # Resume Preview
            with st.expander("👁️ Preview Resume", expanded=True):
                st.components.v1.html(resume_html, height=600, scrolling=True)
            
            st.markdown("---")
            
            # Download Options
            st.markdown("### 📥 Download Options")
            st.caption("Choose your preferred format. All downloads are 100% FREE!")
            
            # Final Checklist & Affirmation
            st.info("""
            🌟 **You're Ready! Final Checklist:**
            
            ✅ Resume has quantified achievements
            
            ✅ Keywords from job description included
            
            ✅ LinkedIn profile matches resume content
            
            ✅ No photos (unless Germany/France)
            
            ✅ Clean, ATS-friendly formatting
            
            💪 **Remember**: You've built something powerful here. Your resume reflects not just your skills, but your growth, resilience, and unique journey. Trust in your value and apply with confidence!
            """)
            
            # File name
            file_base_name = st.session_state.get('full_name', 'Resume').replace(' ', '_')
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # HTML Download
                resume_html_bytes = resume_html.encode('utf-8', errors='ignore')
                st.download_button(
                    "📄 Download HTML",
                    resume_html_bytes,
                    file_name=f"{file_base_name}.html",
                    mime="text/html",
                    use_container_width=True,
                    key="download_html_btn"
                )
                st.caption("✓ Best for web viewing")
            
            with col2:
                # PDF Download
                if PDF_AVAILABLE:
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            pdfkit.from_string(resume_html, tmp.name)
                            with open(tmp.name, "rb") as f:
                                pdf_data = f.read()
                        st.download_button(
                            "📑 Download PDF",
                            pdf_data,
                            file_name=f"{file_base_name}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key="download_pdf_btn"
                        )
                        st.caption("✓ Most popular format")
                    except:
                        st.button("📑 PDF (Install wkhtmltopdf)", disabled=True, use_container_width=True)
                        st.caption("⚠️ PDF generation unavailable")
                else:
                    st.button("📑 PDF (Not Available)", disabled=True, use_container_width=True)
                    st.caption("⚠️ Install pdfkit")
            
            with col3:
                # DOCX Download (using ExportManager)
                try:
                    exporter = ExportManager()
                    docx_data = exporter.export_to_docx(st.session_state)
                    st.download_button(
                        "📝 Download DOCX",
                        docx_data,
                        file_name=f"{file_base_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key="download_docx_btn"
                    )
                    st.caption("✓ Editable in Word")
                except:
                    st.button("📝 DOCX (Install python-docx)", disabled=True, use_container_width=True)
                    st.caption("⚠️ DOCX export unavailable")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Plain Text Export
                resume_text = f"""
{st.session_state.get('full_name', '')}
{st.session_state.get('email', '')} | {st.session_state.get('phone', '')}
{st.session_state.get('city', '')}

PROFESSIONAL SUMMARY
{st.session_state.get('summary', '')}

SKILLS
{st.session_state.get('tech_skills', '')}

WORK EXPERIENCE
"""
                for work in st.session_state.get('work_entries', []):
                    resume_text += f"\n{work.get('title')} - {work.get('company')}\n"
                    resume_text += f"{work.get('start_date')} - {work.get('end_date')}\n"
                    resume_text += f"{work.get('responsibilities', '')}\n"
                
                resume_text += "\n\nEDUCATION\n"
                for edu in st.session_state.get('education_entries', []):
                    resume_text += f"\n{edu.get('degree')} - {edu.get('stream')}\n"
                    resume_text += f"{edu.get('institution')}, {edu.get('year')}\n"
                
                st.download_button(
                    "📃 Download TXT",
                    resume_text.encode('utf-8'),
                    file_name=f"{file_base_name}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="download_txt_btn"
                )
                st.caption("✓ 100% ATS compatible")
            
            with col2:
                # JSON Export
                resume_json = json.dumps({k: v for k, v in dict(st.session_state).items() 
                                         if isinstance(v, (str, int, float, bool, list, dict))}, indent=2)
                st.download_button(
                    "💾 Download JSON",
                    resume_json.encode('utf-8'),
                    file_name=f"{file_base_name}.json",
                    mime="application/json",
                    use_container_width=True,
                    key="download_json_btn"
                )
                st.caption("✓ Data backup")
            
            with col3:
                # Markdown Export
                resume_md = f"""# {st.session_state.get('full_name', '')}

**{st.session_state.get('job_title_target', '')}**

📧 {st.session_state.get('email', '')} | 📱 {st.session_state.get('phone', '')}

## Professional Summary
{st.session_state.get('summary', '')}

## Skills
{st.session_state.get('tech_skills', '')}

## Work Experience
"""
                for work in st.session_state.get('work_entries', []):
                    resume_md += f"\n### {work.get('title')} - {work.get('company')}\n"
                    resume_md += f"*{work.get('start_date')} - {work.get('end_date')}*\n\n"
                    resume_md += f"{work.get('responsibilities', '')}\n"
                
                st.download_button(
                    "📋 Download MD",
                    resume_md.encode('utf-8'),
                    file_name=f"{file_base_name}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key="download_md_btn"
                )
                st.caption("✓ GitHub ready")
            
            st.markdown("---")
            
            # Save to Dashboard
            st.markdown("### 💾 Save to Dashboard")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                resume_name = st.text_input("Resume Name", 
                                           value=f"{st.session_state.get('job_title_target', 'My Resume')} - {datetime.now().strftime('%b %d')}",
                                           key="save_resume_name")
            with col2:
                if st.button("💾 Save Resume", use_container_width=True, key="save_to_dashboard_btn"):
                    # Generate unique ID
                    resume_id = f"resume_{int(time.time())}"
                    
                    # Save to resumes dict
                    if 'resumes' not in st.session_state:
                        st.session_state.resumes = {}
                    
                    st.session_state.resumes[resume_id] = {
                        'name': resume_name,
                        'full_name': st.session_state.get('full_name', ''),
                        'job_title_target': st.session_state.get('job_title_target', ''),
                        'email': st.session_state.get('email', ''),
                        'phone': st.session_state.get('phone', ''),
                        'city': st.session_state.get('city', ''),
                        'summary': st.session_state.get('summary', ''),
                        'tech_skills': st.session_state.get('tech_skills', ''),
                        'work_entries': st.session_state.get('work_entries', []),
                        'education_entries': st.session_state.get('education_entries', []),
                        'selected_template': st.session_state.get('selected_template', ''),
                        'created_at': datetime.now().strftime('%b %d, %Y %I:%M %p'),
                        'completeness': calculate_completeness()
                    }
                    
                    # Save to file
                    with open("soulskill_resumes.json", "w", encoding='utf-8') as f:
                        json.dump(st.session_state.resumes, f, indent=2)
                    
                    st.success(f"✅ Resume saved as '{resume_name}'!")
            
            st.markdown("---")
            
            # Additional Tools
            st.markdown("### 🛠️ Additional Tools")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Generate QR Code
                if st.button("📱 Generate QR Code", use_container_width=True, key="qr_code_btn"):
                    qr_gen = QRCodeGenerator()
                    qr_data = qr_gen.generate_vcard_qr(st.session_state)
                    if qr_data:
                        st.image(qr_data, caption="Scan to save contact", width=200)
                        st.download_button(
                            "Download QR Code",
                            qr_data,
                            file_name=f"{file_base_name}_QR.png",
                            mime="image/png"
                        )
            
            with col2:
                # Email Templates
                if st.button("📧 Get Email Templates", use_container_width=True, key="email_templates_btn"):
                    st.markdown("**📧 Professional Email Templates**")
                    templates = EmailTemplates.get_all_templates(st.session_state)
                    for template_name, template_content in list(templates.items())[:2]:
                        with st.expander(f"📨 {template_name}"):
                            st.text_area("", value=template_content, height=150, key=f"email_{template_name}")
        
        with col_score:
            st.markdown("### 📊 ATS Score Dashboard")
            
            # Job Description Input for ATS
            job_desc = st.text_area(
                "Paste Job Description",
                value=st.session_state.get('job_description', ''),
                height=200,
                placeholder="Paste the job description to get ATS match score...",
                key="job_desc_step4"
            )
            st.session_state.job_description = job_desc
            
            if st.button("🔍 Calculate ATS Score", use_container_width=True, key="calc_ats_btn"):
                if job_desc:
                    with st.spinner("Analyzing..."):
                        # Compile resume text
                        resume_text = f"{st.session_state.get('full_name', '')} {st.session_state.get('job_title_target', '')} {st.session_state.get('summary', '')} {st.session_state.get('tech_skills', '')}"
                        
                        for work in st.session_state.get('work_entries', []):
                            resume_text += f" {work.get('title', '')} {work.get('company', '')} {work.get('responsibilities', '')}"
                        
                        # Calculate ATS score
                        ats_result = ai_assistant.calculate_ats_score(resume_text, job_desc)
                        st.session_state.ats_score = ats_result
                        
                        score = ats_result.get('score', 0)
                        
                        # Display score
                        if score >= 75:
                            st.success(f"🎉 Excellent! ATS Score: {score}/100")
                        elif score >= 50:
                            st.warning(f"👍 Good! ATS Score: {score}/100")
                        else:
                            st.error(f"⚠️ Needs Work: ATS Score: {score}/100")
                        
                        st.metric("Keyword Match", f"{ats_result.get('keyword_match', 0)}%")
                        st.metric("Matched Keywords", f"{ats_result.get('matched_keywords', 0)}/{ats_result.get('total_job_keywords', 0)}")
                        
                        # Missing keywords
                        if ats_result.get('missing_keywords'):
                            st.markdown("**Missing Keywords:**")
                            for kw in ats_result['missing_keywords'][:5]:
                                st.caption(f"❌ {kw}")
                else:
                    st.info("Paste a job description to analyze")
            
            # Show previous score if available
            if st.session_state.get('ats_score'):
                score = st.session_state.ats_score.get('score', 0)
                st.markdown("---")
                st.markdown("### 📈 Your Score")
                st.progress(score / 100)
                st.metric("ATS Score", f"{score}/100")
            
            # Resume Stats
            st.markdown("---")
            st.markdown("### 📊 Resume Stats")
            st.metric("Completeness", f"{calculate_completeness()}%")
            st.metric("Work Positions", len(st.session_state.get('work_entries', [])))
            st.metric("Education", len(st.session_state.get('education_entries', [])))
        
        # Navigation
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⬅️ Back to Customize", use_container_width=True, key="back_from_step4"):
                st.session_state.step = 3
                st.rerun()
        
        with col2:
            if st.button("🏠 Home", use_container_width=True, key="home_from_step4"):
                st.session_state.mode = 'home'
                st.rerun()
        
        with col3:
            if st.button("📂 Dashboard", use_container_width=True, key="dashboard_from_step4"):
                st.session_state.mode = 'dashboard'
                st.rerun()

elif st.session_state.mode == 'coverletter':
    # COVER LETTER BUILDER
    st.markdown("""
    <div class='hero-section' style='padding: 2rem; margin-bottom: 1rem;'>
        <h1 class='hero-title' style='font-size: 2rem;'>✉️ AI Cover Letter Builder</h1>
        <p class='hero-subtitle' style='font-size: 1rem;'>Create compelling cover letters in minutes</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("### 📝 Cover Letter Details")
        
        # Company and Position
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company Name *", value=st.session_state.get('cl_company', ''), 
                                   placeholder="e.g., Google", key="cl_company_input")
            st.session_state.cl_company = company
        with col2:
            position = st.text_input("Position *", value=st.session_state.get('cl_position', ''),
                                    placeholder="e.g., Software Engineer", key="cl_position_input")
            st.session_state.cl_position = position
        
        # Use resume data if available
        if st.session_state.get('full_name'):
            st.info(f"Using your resume data: {st.session_state.get('full_name')} | {st.session_state.get('job_title_target', '')}")
        
        # Cover Letter Templates
        st.markdown("### 📋 Choose Template")
        
        cl_templates = {
            "professional": {
                "name": "Professional",
                "description": "Traditional and formal approach",
                "icon": "👔",
                "template": """Dear Hiring Manager,

I am writing to express my strong interest in the {position} position at {company}. With my background in {field} and proven track record of {achievement}, I am confident in my ability to contribute to your team's success.

In my current role as {current_role}, I have successfully {accomplishment1}. Additionally, I have {accomplishment2}, which directly aligns with the requirements outlined in your job posting.

What particularly excites me about {company} is {company_aspect}. I am impressed by {company_achievement} and would be thrilled to contribute to such innovative work.

I am confident that my skills in {key_skills} make me an ideal candidate for this position. I would welcome the opportunity to discuss how my experience and passion align with {company}'s goals.

Thank you for considering my application. I look forward to the opportunity to discuss this position further.

Sincerely,
{name}"""
            },
            "enthusiastic": {
                "name": "Enthusiastic",
                "description": "Passionate and engaging tone",
                "icon": "🚀",
                "template": """Dear {company} Team,

I'm thrilled to apply for the {position} role at {company}! As a {current_role} with a passion for {passion_area}, I've been following {company}'s work in {company_field} and am genuinely excited about the opportunity to contribute.

Throughout my career, I've demonstrated my commitment to {value1} and {value2}. At {previous_company}, I {achievement}, which resulted in {result}. This experience has prepared me perfectly for the challenges and opportunities at {company}.

What really resonates with me about {company} is {company_value}. Your commitment to {company_mission} aligns perfectly with my professional goals and personal values.

I bring to the table {skill1}, {skill2}, and {skill3}, along with an unwavering drive to deliver exceptional results. I'm confident that my unique blend of skills and enthusiasm would make me a valuable addition to your team.

I'd love the opportunity to discuss how I can contribute to {company}'s continued success. Thank you for your consideration!

Best regards,
{name}"""
            },
            "modern": {
                "name": "Modern",
                "description": "Concise and direct approach",
                "icon": "⚡",
                "template": """Hello,

I'm {name}, and I'm excited to apply for the {position} role at {company}.

Here's why I'm a great fit:

• {bullet_point1}
• {bullet_point2}  
• {bullet_point3}

My background in {field} and experience with {technologies} aligns perfectly with what you're looking for. At {previous_company}, I {key_achievement}.

I've been impressed by {company}'s {company_strength} and would love to contribute to {company_goal}.

Let's talk about how I can help {company} achieve its goals. I'm available at {email} or {phone}.

Looking forward to connecting,
{name}"""
            },
            "creative": {
                "name": "Creative",
                "description": "Unique and memorable style",
                "icon": "🎨",
                "template": """Dear {company} Hiring Team,

Picture this: {creative_opening}

That's the kind of impact I aim to make as your next {position}. With {years} years of experience in {field}, I don't just meet expectations—I exceed them.

My Story:
{background_story}

My Superpowers:
→ {superpower1}
→ {superpower2}
→ {superpower3}

Why {company}?
{company_reason}

I'm not just looking for a job—I'm looking for a place where I can make a real difference. {company} is that place.

Ready to discuss how I can contribute? Let's connect.

Creatively yours,
{name}"""
            }
        }
        
        selected_template = st.selectbox(
            "Select Template Style",
            options=list(cl_templates.keys()),
            format_func=lambda x: f"{cl_templates[x]['icon']} {cl_templates[x]['name']} - {cl_templates[x]['description']}",
            key="cl_template_select"
        )
        
        st.markdown("---")
        
        # AI Generation
        if ai_assistant.enabled:
            st.markdown("### ✨ AI Generation")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🤖 Generate with AI", use_container_width=True, key="generate_cl_ai"):
                    if company and position:
                        with st.spinner("AI is crafting your cover letter..."):
                            # Prepare profile data
                            profile_data = {
                                'name': st.session_state.get('full_name', 'Your Name'),
                                'current_role': st.session_state.get('job_title_target', 'Professional'),
                                'company': company,
                                'position': position,
                                'skills': st.session_state.get('tech_skills', ''),
                                'experience': st.session_state.get('work_entries', [])
                            }
                            
                            # Generate cover letter using AI
                            prompt = f"""Write a professional cover letter for {profile_data['name']} applying for {position} at {company}.
                            
Current role: {profile_data['current_role']}
Skills: {profile_data['skills']}

The letter should be compelling, specific, and highlight relevant experience. Keep it under 400 words."""
                            
                            try:
                                cl_content = ai_assistant.model.generate_content(prompt).text
                                st.session_state.cl_content = cl_content
                                st.success("✅ Cover letter generated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"AI generation failed: {str(e)}")
                    else:
                        st.warning("Please enter company name and position first")
            
            with col2:
                if st.button("🔄 Use Template", use_container_width=True, key="use_cl_template"):
                    # Fill template with data
                    template_text = cl_templates[selected_template]['template']
                    
                    # Replace placeholders
                    replacements = {
                        '{name}': st.session_state.get('full_name', 'Your Name'),
                        '{position}': position or '[Position]',
                        '{company}': company or '[Company]',
                        '{email}': st.session_state.get('email', '[your email]'),
                        '{phone}': st.session_state.get('phone', '[your phone]'),
                        '{current_role}': st.session_state.get('job_title_target', '[your role]'),
                        '{field}': st.session_state.get('industry', '[your field]'),
                        '{key_skills}': st.session_state.get('tech_skills', '[your skills]').split(',')[0] if st.session_state.get('tech_skills') else '[skills]',
                        '{achievement}': 'delivering successful projects',
                        '{accomplishment1}': 'exceeded performance goals',
                        '{accomplishment2}': 'led successful initiatives',
                        '{company_aspect}': 'your innovative approach',
                        '{company_achievement}': 'your recent accomplishments',
                        '{passion_area}': 'innovation and excellence',
                        '{company_field}': 'your industry',
                        '{value1}': 'quality',
                        '{value2}': 'innovation',
                        '{previous_company}': st.session_state.get('work_entries', [{}])[0].get('company', '[Previous Company]') if st.session_state.get('work_entries') else '[Previous Company]',
                        '{result}': 'significant improvements',
                        '{company_value}': 'your values',
                        '{company_mission}': 'your mission',
                        '{skill1}': st.session_state.get('tech_skills', 'skills').split(',')[0] if st.session_state.get('tech_skills') else 'expertise',
                        '{skill2}': 'experience',
                        '{skill3}': 'dedication',
                        '{years}': '5+',
                        '{technologies}': st.session_state.get('tech_skills', '[technologies]'),
                        '{key_achievement}': 'achieved significant results',
                        '{company_strength}': 'innovative work',
                        '{company_goal}': 'future goals',
                        '{creative_opening}': 'A passionate professional ready to make an impact',
                        '{background_story}': 'I have built a career focused on excellence and innovation',
                        '{superpower1}': 'Problem-solving',
                        '{superpower2}': 'Team collaboration',
                        '{superpower3}': 'Results delivery',
                        '{company_reason}': f"{company} represents the perfect opportunity to apply my skills",
                        '{bullet_point1}': f"Expertise in {st.session_state.get('industry', 'the field')}",
                        '{bullet_point2}': 'Proven track record of success',
                        '{bullet_point3}': 'Passionate about driving results'
                    }
                    
                    for key, value in replacements.items():
                        template_text = template_text.replace(key, str(value))
                    
                    st.session_state.cl_content = template_text
                    st.success("✅ Template applied!")
                    st.rerun()
        else:
            st.warning("⚠️ AI features offline. Using templates instead.")
        
        st.markdown("---")
        
        # Manual editing
        st.markdown("### ✍️ Edit Cover Letter")
        cl_content = st.text_area(
            "Cover Letter Content",
            value=st.session_state.get('cl_content', ''),
            height=400,
            placeholder="Write your cover letter here or use AI/Templates above...",
            key="cl_content_input",
            help="Type your content - it saves automatically"
        )
        
        # Auto-save functionality
        if cl_content != st.session_state.get('cl_content', ''):
            st.session_state.cl_content = cl_content
            st.caption("💾 Auto-saved")
        
        # Word count
        if cl_content:
            word_count = len(cl_content.split())
            char_count = len(cl_content)
            col_w1, col_w2 = st.columns(2)
            with col_w1:
                st.caption(f"📊 {word_count} words • {char_count} characters")
            with col_w2:
                if word_count > 500:
                    st.caption("⚠️ Consider shortening (250-400 ideal)")
                elif word_count < 200:
                    st.caption("💡 Add more details (250-400 ideal)")
                else:
                    st.caption("✅ Great length!")
        
        st.markdown("---")
        
        # Download Options
        st.markdown("### 📥 Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if cl_content:
                file_name = f"CoverLetter_{company.replace(' ', '_')}_{position.replace(' ', '_')}"
                st.download_button(
                    "📄 Download TXT",
                    cl_content.encode('utf-8'),
                    file_name=f"{file_name}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="download_cl_txt"
                )
        
        with col2:
            if cl_content:
                # Simple HTML version
                cl_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 2rem; max-width: 800px; margin: 0 auto; line-height: 1.6; }}
        .header {{ margin-bottom: 2rem; }}
        .content {{ white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>{st.session_state.get('full_name', 'Your Name')}</h2>
        <p>{st.session_state.get('email', '')} | {st.session_state.get('phone', '')}</p>
    </div>
    <div class="content">{cl_content}</div>
</body>
</html>
"""
                st.download_button(
                    "📄 Download HTML",
                    cl_html.encode('utf-8'),
                    file_name=f"{file_name}.html",
                    mime="text/html",
                    use_container_width=True,
                    key="download_cl_html"
                )
        
        with col3:
            if cl_content and PDF_AVAILABLE:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        pdfkit.from_string(cl_html, tmp.name)
                        with open(tmp.name, "rb") as f:
                            pdf_data = f.read()
                    st.download_button(
                        "📑 Download PDF",
                        pdf_data,
                        file_name=f"{file_name}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_cl_pdf"
                    )
                except:
                    st.button("📑 PDF (Unavailable)", disabled=True, use_container_width=True)
    
    with col_preview:
        st.markdown("### 👁️ Live Preview")
        
        if cl_content:
            # Display preview
            preview_html = f"""
<div style='background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); min-height: 600px;'>
    <div style='margin-bottom: 2rem; border-bottom: 2px solid #667eea; padding-bottom: 1rem;'>
        <h2 style='margin: 0; color: #333;'>{st.session_state.get('full_name', 'Your Name')}</h2>
        <p style='margin: 0.5rem 0 0 0; color: #666;'>{st.session_state.get('email', '')} | {st.session_state.get('phone', '')}</p>
        <p style='margin: 0.25rem 0 0 0; color: #666;'>{st.session_state.get('city', '')}</p>
    </div>
    <div style='margin-bottom: 2rem;'>
        <p style='margin: 0; color: #666;'>{datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    <div style='margin-bottom: 2rem;'>
        <p style='margin: 0; font-weight: 600; color: #333;'>{company if company else '[Company Name]'}</p>
        <p style='margin: 0.25rem 0 0 0; color: #666;'>Hiring Manager</p>
    </div>
    <div style='white-space: pre-wrap; line-height: 1.8; color: #333;'>
{cl_content}
    </div>
</div>
"""
            st.components.v1.html(preview_html, height=650, scrolling=True)
        else:
            st.info("📝 Your cover letter preview will appear here")
            st.caption("Fill in the details and use AI or templates to generate content")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home", use_container_width=True, key="cl_home_btn"):
            st.session_state.mode = 'home'
            st.rerun()
    with col2:
        if st.button("📂 Dashboard", use_container_width=True, key="cl_dashboard_btn"):
            st.session_state.mode = 'dashboard'
            st.rerun()
    with col3:
        if st.button("🎓 Masters SOP", use_container_width=True, key="cl_masters_btn"):
            st.session_state.mode = 'masters'
            st.rerun()

elif st.session_state.mode == 'masters':
    # MASTERS/SOP LETTER BUILDER
    st.markdown("""
    <div class='hero-section' style='padding: 2rem; margin-bottom: 1rem;'>
        <h1 class='hero-title' style='font-size: 2rem;'>🎓 Statement of Purpose Builder</h1>
        <p class='hero-subtitle' style='font-size: 1rem;'>Create compelling applications for graduate programs</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("### 📝 Application Details")
        
        # University and Program
        col1, col2 = st.columns(2)
        with col1:
            university = st.text_input("University Name *", value=st.session_state.get('sop_university', ''), 
                                   placeholder="e.g., Stanford University", key="sop_university_input")
            st.session_state.sop_university = university
        with col2:
            program = st.text_input("Program *", value=st.session_state.get('sop_program', ''),
                                    placeholder="e.g., MS in Computer Science", key="sop_program_input")
            st.session_state.sop_program = program
        
        # Personal details
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name *", value=st.session_state.get('full_name', ''),
                               placeholder="John Doe", key="sop_name_input")
        with col2:
            email = st.text_input("Email *", value=st.session_state.get('email', ''),
                                placeholder="john@email.com", key="sop_email_input")
        
        st.markdown("---")
        st.markdown("### ✍️ Edit Statement of Purpose")
        sop_content = st.text_area(
            "SOP Content",
            value=st.session_state.get('sop_content', ''),
            height=450,
            placeholder="Write your statement of purpose here...",
            key="sop_text_area"
        )
        st.session_state.sop_content = sop_content
        
        # Export options
        st.markdown("### 💾 Save & Export")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Text", use_container_width=True):
                st.success("✅ Select and copy the text above!")
        with col2:
            if sop_content:
                st.download_button(
                    "📥 Download TXT",
                    sop_content,
                    file_name=f"SOP_{program.replace(' ', '_') if program else 'Statement'}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    with col_preview:
        st.markdown("### 👁️ Live Preview")
        
        if sop_content:
            # Display preview
            preview_html = f"""
<div style='background: white; padding: 2.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); font-family: "Times New Roman", serif; max-width: 800px; margin: 0 auto;'>
    <div style='margin-bottom: 2rem; text-align: right;'>
        <p style='margin: 0; font-weight: 600; color: #333;'>{name if name else '[Your Name]'}</p>
        <p style='margin: 0.25rem 0 0 0; color: #666;'>{email if email else '[Your Email]'}</p>
    </div>
    <div style='margin-bottom: 2rem;'>
        <p style='margin: 0; color: #666;'>{datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    <div style='margin-bottom: 2rem;'>
        <p style='margin: 0; font-weight: 600; color: #333;'>Admissions Committee</p>
        <p style='margin: 0.25rem 0 0 0; color: #666;'>{program if program else '[Program]'}</p>
        <p style='margin: 0.25rem 0 0 0; color: #666;'>{university if university else '[University]'}</p>
    </div>
    <div style='white-space: pre-wrap; line-height: 1.8; color: #333;'>
{sop_content}
    </div>
</div>
"""
            st.components.v1.html(preview_html, height=650, scrolling=True)
        else:
            st.info("📝 Your statement of purpose preview will appear here")
            st.caption("Fill in the details above to see preview")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home", use_container_width=True, key="sop_home_btn"):
            st.session_state.mode = 'home'
            st.rerun()
    with col2:
        if st.button("📄 Build Resume", use_container_width=True, key="sop_resume_btn"):
            st.session_state.mode = 'builder'
            st.session_state.step = 1
            st.rerun()
    with col3:
        if st.button("✉️ Cover Letter", use_container_width=True, key="sop_cl_btn"):
            st.session_state.mode = 'coverletter'
            st.rerun()

elif st.session_state.mode == 'about':
    # About Page
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🚀</div>
        <h1 style='font-size: 3rem; font-weight: 900; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            About SoulSkill
        </h1>
        <p style='font-size: 1.3rem; color: #4a5568; font-weight: 600; margin-top: 1rem;'>
            Your AI-Powered Career Companion
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        ### 🎯 Our Mission
        
        **SoulSkill** is more than just a resume builder - it's your complete career success platform. 
        We believe that everyone deserves a professional, ATS-optimized resume that showcases their 
        unique skills and experiences, without the need for expensive services or design skills.
        
        ### ✨ What Makes Us Different
        
        **🤖 AI-Powered Intelligence**
        - Smart content generation using Google Gemini AI
        - ATS optimization with real-time scoring
        - Personalized suggestions based on your role and industry
        
        **🎨 Professional Templates**
        - 35+ professionally designed templates
        - Global templates (India, US, UK, Canada, Australia, UAE, Singapore)
        - Industry-specific designs
        - One-click template switching
        
        **💼 Complete Career Tools**
        - Resume builder with AI assistance
        - Cover letter generator
        - ATS score checker
        - Content library with proven examples
        - Multi-resume management dashboard
        
        **🆓 100% Free Forever**
        - No credit card required
        - No hidden fees or premium plans
        - All features available to everyone
        - Export to PDF, DOCX, or HTML
        
        ### 📊 By The Numbers
        """)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Users Helped", "50,000+", "Growing daily")
        with col_b:
            st.metric("Resumes Created", "15,000+", "This month")
        with col_c:
            st.metric("Success Rate", "95%", "ATS Pass Rate")
        
        st.markdown("""
        ### 🌟 Our Story
        
        SoulSkill was born from a simple idea: **job hunting shouldn't be harder than the job itself**.
        
        We saw talented professionals struggling with:
        - Expensive resume services (₹2000-₹5000 per resume)
        - Complex design tools requiring hours to master
        - Resumes getting rejected by ATS systems
        - No guidance on what makes a great resume
        
        So we built **SoulSkill** - combining cutting-edge AI technology with professional resume 
        design expertise to make creating a winning resume as simple as filling out a form.
        
        ### 🚀 Technology Stack
        
        - **AI Engine**: Google Gemini Pro for intelligent content generation
        - **Frontend**: Streamlit for fast, responsive user experience
        - **Templates**: Professional HTML/CSS designs optimized for ATS
        - **Export**: Multi-format support (PDF, DOCX, HTML)
        
        ### 💡 Our Values
        
        **🌈 Accessibility**: Career tools should be free and available to everyone
        
        **👨 Quality**: Professional results without compromising on quality
        
        **🤝 User-First**: Built with feedback from real job seekers
        
        **🔒 Privacy**: Your data is yours - we never share or sell it
        
        **⚡ Innovation**: Constantly improving with the latest AI technology
        
        ### 🎓 Who We Help
        
        - **Fresh Graduates**: Launch your career with a standout resume
        - **Professionals**: Advance your career with ATS-optimized resumes
        - **Career Changers**: Highlight transferable skills effectively
        - **Freelancers**: Showcase diverse experience professionally
        - **International Job Seekers**: Templates for multiple countries
        
        ### 🌍 Global Reach
        
        We serve job seekers worldwide with localized templates and content for:
        - 🇮🇳 India (Mumbai, Bangalore, Delhi, Hyderabad, Pune)
        - 🇺🇸 United States
        - 🇬🇧 United Kingdom  
        - 🇨🇦 Canada
        - 🇦🇺 Australia
        - 🇦🇪 UAE
        - 🇸🇬 Singapore
        
        ### 💚 Thank You
        
        Thank you for choosing **SoulSkill**. We're honored to be part of your career journey.
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Building Now", use_container_width=True, type="primary", key="about_cta"):
            st.session_state.mode = 'builder'
            st.session_state.step = 1
            st.rerun()

elif st.session_state.mode == 'contact':
    # Contact Us Page
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>📧</div>
        <h1 style='font-size: 3rem; font-weight: 900; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Contact Us
        </h1>
        <p style='font-size: 1.3rem; color: #4a5568; font-weight: 600; margin-top: 1rem;'>
            We'd Love to Hear From You!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        ### 💬 Get in Touch
        
        Have questions, feedback, or need help? We're here for you!
        
        ### 📧 Email Us
        
        For any inquiries, support requests, or feedback, reach out to us at:
        """)
        
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    border-radius: 15px; margin: 2rem 0; border: 2px solid #667eea;'>
            <p style='font-size: 0.9rem; color: #666; margin-bottom: 0.5rem; font-weight: 600;'>Official Email</p>
            <a href='mailto:soulvest1111@gmail.com' style='font-size: 1.5rem; font-weight: 700; color: #667eea; text-decoration: none;'>
                📧 soulvest1111@gmail.com
            </a>
            <p style='font-size: 0.85rem; color: #666; margin-top: 1rem;'>Click to send us an email</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 🤝 How We Can Help
        
        **💡 General Inquiries**
        - Questions about features
        - Partnership opportunities
        - Media inquiries
        
        **🐛 Technical Support**
        - Bug reports
        - Feature requests
        - Technical issues
        
        **💼 Career Services**
        - Resume review feedback
        - Template suggestions
        - Career advice
        
        **🌟 Feedback & Suggestions**
        - Share your experience
        - Suggest new features
        - Template requests
        
        ### ⏰ Response Time
        
        We typically respond within:
        - **24 hours** for general inquiries
        - **48 hours** for technical issues
        - **72 hours** during peak periods
        
        ### 🌐 Connect With Us
        
        Stay updated with the latest features and career tips!
        
        ### 📝 Quick Contact Form
        
        Send us a message directly:
        """)
        
        with st.form("contact_form", clear_on_submit=True):
            contact_name = st.text_input("Your Name *", placeholder="John Doe")
            contact_email = st.text_input("Your Email *", placeholder="your@email.com")
            contact_subject = st.selectbox(
                "Subject *",
                ["", "General Inquiry", "Technical Support", "Feature Request", 
                 "Bug Report", "Partnership", "Feedback", "Other"]
            )
            contact_message = st.text_area(
                "Message *",
                placeholder="Tell us how we can help you...",
                height=150
            )
            
            submitted = st.form_submit_button("📤 Send Message", use_container_width=True, type="primary")
            
            if submitted:
                if not contact_name or not contact_email or not contact_subject or not contact_message:
                    st.error("❌ Please fill in all fields")
                elif "@" not in contact_email:
                    st.error("❌ Please enter a valid email address")
                else:
                    st.success("✅ Thank you for your message!")
                    st.info("📧 Your message has been prepared. Click below to send via email:")
                    
                    mailto_link = f"mailto:soulvest1111@gmail.com?subject={contact_subject} - {contact_name}&body=From: {contact_name} ({contact_email})%0A%0A{contact_message}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.75rem 2rem; border-radius: 10px; border: none; font-weight: 600; cursor: pointer; font-size: 1rem; width: 100%;">📬 Open Email Client</button></a>', unsafe_allow_html=True)
                    st.caption("Or copy and paste: soulvest1111@gmail.com")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        
        if st.button("📄 Build Resume", use_container_width=True, type="primary", key="contact_cta"):
            st.session_state.mode = 'builder'
            st.session_state.step = 1
            st.rerun()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); border-radius: 15px; margin-top: 2rem;'>
    <p style='font-size: 1.2rem; font-weight: 700; color: #2d3748; margin-bottom: 0.5rem;'>
        <strong>✨ Soulvest AI Resume Builder</strong> - Build Your Resume in 5 Minutes
    </p>
    <p style='font-size: 1rem; font-weight: 600; color: #4a5568; margin-bottom: 1rem;'>
        <strong>© 2026 Soulvest.ai • 100% Free Forever • No Credit Card Required</strong>
    </p>
    <p style='font-size: 0.9rem; color: #718096; margin-top: 1rem;'>
        Made with ❤️ for job seekers worldwide
    </p>
</div>
""", unsafe_allow_html=True)
