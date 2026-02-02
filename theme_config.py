"""
Enhanced Theme Configuration for SoulSkill
"""

# Custom CSS for enhanced UI
ENHANCED_CSS = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');
    
    /* Set default font for entire app */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Use Poppins for headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main app background (clean, professional with subtle pattern) */
    .main {
        background: linear-gradient(135deg, #f5f7fb 0%, #e8eef7 100%);
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(37, 99, 235, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(29, 78, 216, 0.02) 0%, transparent 50%);
        background-attachment: fixed;
    }
    
    /* Content area */
    .block-container {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 24px 0 rgba(15, 23, 42, 0.08);
        border: 1px solid #e5e7eb;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #2563eb 100%);
        color: white !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown div {
        color: white !important;
    }
    
    /* Sidebar text colors - all elements */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stCaption {
        color: white !important;
    }
    
    /* Sidebar expander styling */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.15);
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader p {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent {
        background-color: rgba(255, 255, 255, 0.08);
        color: white !important;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent * {
        color: white !important;
    }
    
    /* Sidebar checkboxes */
    [data-testid="stSidebar"] .stCheckbox label {
        color: white !important;
    }
    
    /* Sidebar dividers */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Headers with gradient text (main content only, not sidebar) */
    .main h1 {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Ensure main content text is visible */
    .main h2 {
        color: #2d3748 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        background: none !important;
        -webkit-text-fill-color: #2d3748 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    .main h3 {
        color: #2d3748 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        background: none !important;
        -webkit-text-fill-color: #2d3748 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    .main h4, .main h5, .main h6 {
        color: #4a5568 !important;
        font-weight: 600 !important;
        background: none !important;
        -webkit-text-fill-color: #4a5568 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    /* Ensure paragraph text is dark and readable */
    .main p {
        color: #2d3748 !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
    }
    
    .main .stMarkdown p {
        color: #2d3748 !important;
    }
    
    /* Buttons - Main content */
    .stButton>button {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(29, 78, 216, 0.35);
        cursor: pointer;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px 0 rgba(29, 78, 216, 0.45);
    }
    
    /* Sidebar buttons specifically */
    [data-testid="stSidebar"] .stButton>button {
        background: rgba(255, 255, 255, 0.2);
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
    }
    
    /* Cards and containers */
    .css-1r6slb0 {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .css-1r6slb0:hover {
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    /* Input fields - modern and visible */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        color: #2d3748 !important;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* Text area specific */
    .stTextArea>div>div>textarea {
        min-height: 120px;
        line-height: 1.6;
    }
    
    /* Select boxes */
    .stSelectbox>div>div>select {
        cursor: pointer;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 8px;
        border-radius: 10px;
    }
    
    /* Metrics - larger and more prominent */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #4a5568 !important;
    }
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Success/Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    /* Template preview cards */
    .template-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .template-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main > div {
        animation: fadeIn 0.5s ease;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Floating action button style */
    .floating-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .floating-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.7);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    /* Step indicator */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
    }
    
    .step {
        flex: 1;
        text-align: center;
        position: relative;
    }
    
    .step::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 2px;
        background: #e0e0e0;
        z-index: -1;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: white;
        border: 3px solid #e0e0e0;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .step.active .step-circle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    
    .step.completed .step-circle {
        background: #4caf50;
        color: white;
        border-color: #4caf50;
    }
    
    /* Dashboard Cards - Feature Cards */
    .dashboard-card {
        background: white;
        border-radius: 15px;
        padding: 1.75rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        height: 100%;
        min-height: 180px;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }
    
    .dashboard-card h3 {
        color: #2d3748 !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.75rem !important;
        background: none !important;
        -webkit-text-fill-color: #2d3748 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    .dashboard-card p {
        color: #4a5568 !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
    
    /* Hero Section - Homepage */
    .hero-section {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem !important;
        line-height: 1.2 !important;
    }
    
    .hero-subtitle {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #2d3748 !important;
        margin-bottom: 0 !important;
    }
    
    /* Stats Section */
    .stat-item {
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
    }
    
    .stat-number {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
        display: block;
    }
    
    .stat-label {
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #4a5568 !important;
        display: block;
    }
    
    /* Info Boxes - How It Works Cards */
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 15px;
        padding: 1.75rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 2px solid rgba(102, 126, 234, 0.2);
        height: 100%;
        min-height: 180px;
    }
    
    .info-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }
    
    .info-box h2 {
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        color: #2d3748 !important;
        background: none !important;
        -webkit-text-fill-color: initial !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    .info-box h4 {
        color: #2d3748 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.75rem !important;
        background: none !important;
        -webkit-text-fill-color: #2d3748 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    .info-box p {
        color: #4a5568 !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
</style>
"""

# Decorative background patterns
BACKGROUND_PATTERNS = """
<style>
    /* Animated background shapes */
    .main::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
        animation: backgroundMove 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes backgroundMove {
        0%, 100% {
            transform: translate(0, 0);
        }
        50% {
            transform: translate(50px, 50px);
        }
    }
</style>
"""

def apply_custom_theme():
    """Apply the custom theme to the Streamlit app"""
    import streamlit as st
    st.markdown(ENHANCED_CSS, unsafe_allow_html=True)
    st.markdown(BACKGROUND_PATTERNS, unsafe_allow_html=True)
