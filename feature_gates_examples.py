"""
Feature Gates Implementation Examples
Quick reference for protecting premium features in SoulSkill
"""

import streamlit as st
from payment_handler import SubscriptionManager, PRICING_PLANS
from database import get_db_manager
from pricing_ui import show_upgrade_prompt


# ========================================
# EXAMPLE 1: Protect Premium Templates
# ========================================

def render_template_selector():
    """Show templates with premium badge and access control"""
    
    # Free templates - always accessible
    st.subheader("📄 Free Templates")
    for template_id, template in FREE_TEMPLATES.items():
        if st.button(f"{template['name']}", key=f"free_{template_id}"):
            st.session_state.selected_template = template_id
            st.success(f"✅ Selected: {template['name']}")
    
    # Premium templates - require subscription
    st.subheader("💎 Premium Templates")
    
    for template_id, template in PREMIUM_TEMPLATES.items():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{template['name']}** - {template['description']}")
        
        with col2:
            if st.button("Select", key=f"premium_{template_id}"):
                # Check access
                if check_premium_access('premium_templates'):
                    st.session_state.selected_template = template_id
                    st.success(f"✅ Selected: {template['name']}")
                    st.rerun()
                else:
                    # Access denied - show upgrade prompt
                    show_upgrade_prompt("Premium Templates")


# ========================================
# EXAMPLE 2: Limit Free Downloads
# ========================================

def handle_resume_download():
    """Download resume with usage tracking"""
    
    if not st.session_state.user_authenticated:
        st.warning("⚠️ Please sign in to download your resume")
        return
    
    user_email = st.session_state.user_email
    db = get_db_manager()
    sub_manager = SubscriptionManager(db)
    
    # Check and increment usage
    can_download, remaining = sub_manager.increment_usage(
        user_email, 
        'downloads'
    )
    
    if not can_download:
        st.error("❌ Monthly download limit reached!")
        show_upgrade_prompt("Unlimited Downloads")
        return
    
    # Proceed with download
    resume_html = generate_resume_html()
    pdf_bytes = generate_pdf(resume_html)
    
    st.download_button(
        label="📥 Download PDF",
        data=pdf_bytes,
        file_name="resume.pdf",
        mime="application/pdf"
    )
    
    # Show remaining downloads
    if remaining >= 0:
        st.info(f"📊 You have {remaining} downloads remaining this month")
    else:
        st.success("✅ Downloaded! (Unlimited with Premium)")


# ========================================
# EXAMPLE 3: AI Suggestions Gate
# ========================================

def show_ai_suggestions_button():
    """Show AI suggestions with access control"""
    
    if st.button("✨ Get AI Suggestions", type="primary"):
        # Check feature access
        if not check_premium_access('ai_suggestions'):
            show_upgrade_prompt("AI-Powered Suggestions")
            return
        
        # Generate AI suggestions
        with st.spinner("🤖 Generating AI suggestions..."):
            suggestions = generate_ai_suggestions(st.session_state.work_description)
            
            st.success("✅ AI Suggestions Generated!")
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"**{i}.** {suggestion}")
                if st.button(f"Use this", key=f"ai_sugg_{i}"):
                    st.session_state.work_description = suggestion
                    st.rerun()


# ========================================
# EXAMPLE 4: Version Control Feature
# ========================================

def render_version_control():
    """Show resume version history"""
    
    st.subheader("📚 Resume Version History")
    
    # Check access to version control
    has_access, message = check_feature_access('version_control')
    
    if not has_access:
        st.info("💎 Version control is a Premium feature")
        show_upgrade_prompt("Resume Version Control")
        
        # Show limited preview
        st.write("Preview: You have 1 current version saved")
        return
    
    # Show full version history for premium users
    versions = get_resume_versions(st.session_state.user_email)
    
    for version in versions:
        with st.expander(f"Version {version['number']} - {version['date']}"):
            st.write(version['summary'])
            if st.button(f"Restore", key=f"restore_{version['id']}"):
                restore_version(version['id'])
                st.success("✅ Version restored!")
                st.rerun()


# ========================================
# EXAMPLE 5: Advanced ATS Analysis
# ========================================

def show_ats_score():
    """Display ATS score with basic/advanced analysis"""
    
    # Basic ATS score - available to all
    basic_score = calculate_basic_ats_score()
    
    st.metric("ATS Score", f"{basic_score}%")
    st.progress(basic_score / 100)
    
    # Basic tips
    st.write("**Basic Tips:**")
    st.write("✅ Use standard section headings")
    st.write("✅ Include relevant keywords")
    st.write("✅ Keep formatting simple")
    
    # Advanced analysis - premium only
    st.markdown("---")
    st.subheader("🔍 Advanced ATS Analysis")
    
    if check_premium_access('advanced_ats'):
        # Show detailed analysis
        advanced_score = calculate_advanced_ats_score()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Keyword Match", f"{advanced_score['keywords']}%")
        with col2:
            st.metric("Format Score", f"{advanced_score['format']}%")
        with col3:
            st.metric("Content Quality", f"{advanced_score['content']}%")
        
        # Detailed recommendations
        st.write("**Detailed Recommendations:**")
        for rec in advanced_score['recommendations']:
            st.write(f"• {rec}")
    else:
        # Show locked state
        st.info("💎 Unlock advanced ATS analysis with Premium")
        st.write("Get detailed insights:")
        st.write("🔒 Keyword density analysis")
        st.write("🔒 Industry-specific recommendations")
        st.write("🔒 Competitive comparison")
        show_upgrade_prompt("Advanced ATS Analysis")


# ========================================
# EXAMPLE 6: Trial Banner
# ========================================

def show_trial_banner():
    """Show trial status banner"""
    
    if not st.session_state.user_authenticated:
        return
    
    user_email = st.session_state.user_email
    db = get_db_manager()
    sub_manager = SubscriptionManager(db)
    
    subscription = sub_manager.get_user_subscription(user_email)
    
    if subscription['status'] == 'trial':
        # Calculate days remaining
        trial_end = datetime.fromisoformat(subscription['trial_ends_at'])
        days_left = (trial_end - datetime.now()).days
        
        if days_left > 0:
            st.info(f"""
            🎉 **Trial Active!** You have {days_left} days left in your free trial.
            Enjoying Premium? [Upgrade now](?mode=pricing) to continue after trial.
            """)
        else:
            st.warning("""
            ⏰ **Trial Expired!** Your free trial has ended.
            [Upgrade to Premium](?mode=pricing) to continue using premium features.
            """)
    
    elif subscription['plan'] == 'free':
        # Show upgrade banner for free users
        st.info("""
        💎 **Upgrade to Premium** and unlock 20+ templates, AI suggestions, unlimited downloads.
        [Start 7-Day Free Trial](?mode=pricing)
        """)


# ========================================
# EXAMPLE 7: Feature Lock Overlay
# ========================================

def render_locked_feature(feature_name, preview_image=None):
    """Render a locked feature with overlay"""
    
    # Container with blur effect
    with st.container():
        st.markdown("""
        <style>
        .locked-feature {
            position: relative;
            padding: 2rem;
            background: #f7fafc;
            border-radius: 15px;
            border: 2px dashed #cbd5e0;
        }
        .locked-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.9);
            backdrop-filter: blur(5px);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 15px;
        }
        .lock-icon {
            font-size: 3rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Show preview (blurred)
        if preview_image:
            st.image(preview_image, use_column_width=True)
        else:
            st.write("🔒 Premium Feature Preview")
            st.write("This feature is locked")
        
        # Lock overlay
        st.markdown("""
        <div class="locked-overlay">
            <div style="text-align: center;">
                <div class="lock-icon">🔒</div>
                <h3>Premium Feature</h3>
                <p>Upgrade to access {feature_name}</p>
            </div>
        </div>
        """.format(feature_name=feature_name), unsafe_allow_html=True)
        
        # Upgrade button
        if st.button(f"🚀 Unlock {feature_name}", key=f"unlock_{feature_name}"):
            st.session_state.mode = 'pricing'
            st.rerun()


# ========================================
# HELPER FUNCTIONS
# ========================================

def check_premium_access(feature_name):
    """
    Check if user has access to premium feature
    Returns True if access granted, False otherwise
    """
    if not st.session_state.get('user_authenticated', False):
        st.warning("⚠️ Please sign in to access this feature")
        return False
    
    user_email = st.session_state.user_email
    db = get_db_manager()
    sub_manager = SubscriptionManager(db)
    
    has_access, message = sub_manager.check_feature_access(user_email, feature_name)
    
    return has_access


def check_feature_access(feature_name):
    """
    Check feature access and return detailed status
    Returns (has_access: bool, message: str)
    """
    if not st.session_state.get('user_authenticated', False):
        return False, "Please sign in to continue"
    
    user_email = st.session_state.user_email
    db = get_db_manager()
    sub_manager = SubscriptionManager(db)
    
    return sub_manager.check_feature_access(user_email, feature_name)


def get_user_plan_name():
    """Get current user's plan name for display"""
    if not st.session_state.get('user_authenticated', False):
        return "Free"
    
    user_email = st.session_state.user_email
    db = get_db_manager()
    sub_manager = SubscriptionManager(db)
    
    subscription = sub_manager.get_user_subscription(user_email)
    plan = subscription['plan']
    
    if subscription['is_trial']:
        return f"{PRICING_PLANS[plan]['name']} (Trial)"
    
    return PRICING_PLANS[plan]['name']


# ========================================
# USAGE IN MAIN APP
# ========================================

# Add to app_enhanced.py:

"""
# Show trial banner at top of app
show_trial_banner()

# Protect template selection
if selected_template in PREMIUM_TEMPLATES:
    if not check_premium_access('premium_templates'):
        show_upgrade_prompt("Premium Templates")
        st.stop()

# Limit downloads
if st.button("Download Resume"):
    handle_resume_download()

# Gate AI features
if st.button("✨ AI Suggestions"):
    if not check_premium_access('ai_suggestions'):
        show_upgrade_prompt("AI Suggestions")
    else:
        show_ai_suggestions()

# Show user's plan
st.sidebar.write(f"**Plan:** {get_user_plan_name()}")
if get_user_plan_name() == "Free":
    if st.sidebar.button("⬆️ Upgrade"):
        st.session_state.mode = 'pricing'
        st.rerun()
"""
