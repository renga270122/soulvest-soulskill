"""
Authentication UI Components for SoulSkill Resume Builder
"""
import streamlit as st
from auth import get_auth_manager

def show_signin_signup_modal():
    """Display sign-in/sign-up modal dialog"""
    auth = get_auth_manager()
    
    st.markdown("""
    <style>
        .auth-modal {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            margin: 2rem auto;
        }
        .auth-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .auth-header h2 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .auth-benefits {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
        }
        .benefit-item {
            display: flex;
            align-items: center;
            margin: 0.75rem 0;
            font-size: 0.95rem;
        }
        .benefit-icon {
            font-size: 1.5rem;
            margin-right: 0.75rem;
        }
        .divider {
            text-align: center;
            margin: 1.5rem 0;
            position: relative;
        }
        .divider::before {
            content: '';
            position: absolute;
            left: 0;
            right: 0;
            top: 50%;
            height: 1px;
            background: #e0e0e0;
        }
        .divider span {
            background: white;
            padding: 0 1rem;
            position: relative;
            color: #666;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="auth-modal">', unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        <div class="auth-header">
            <h2>✨ Join SoulSkill</h2>
            <p style="color: #666; font-size: 1rem;">Sign up to save and manage your resumes</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Benefits section
        st.markdown("""
        <div class="auth-benefits">
            <div class="benefit-item">
                <span class="benefit-icon">💾</span>
                <span><b>Save unlimited resumes</b> - Access from any device</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-icon">📊</span>
                <span><b>Track your applications</b> - See which resumes perform best</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-icon">🤖</span>
                <span><b>AI-powered suggestions</b> - Get personalized content</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-icon">🔒</span>
                <span><b>100% secure</b> - Your data is encrypted and private</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tab selection
        tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Sign Up"])
        
        with tab1:
            # Sign In Form
            st.markdown("### Welcome Back!")
            
            with st.form("signin_form", clear_on_submit=False):
                email = st.text_input(
                    "Email Address",
                    placeholder="your@email.com",
                    key="signin_email"
                )
                
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="signin_password"
                )
                
                col1, col2 = st.columns([3, 2])
                with col1:
                    remember_me = st.checkbox("Remember me", value=True)
                with col2:
                    st.markdown('<p style="text-align: right; font-size: 0.85rem;"><a href="#forgot">Forgot password?</a></p>', unsafe_allow_html=True)
                
                signin_submit = st.form_submit_button("🔐 Sign In", use_container_width=True, type="primary")
                
                if signin_submit:
                    if not email or not password:
                        st.error("❌ Please fill in all fields")
                    elif len(password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        if auth.login_with_email(email, password):
                            st.session_state.user_authenticated = True
                            st.session_state.user_email = email
                            st.session_state.user_name = email.split('@')[0]
                            st.session_state.show_auth_modal = False
                            st.success("✅ Signed in successfully!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
            
            # OAuth options
            st.markdown('<div class="divider"><span>or continue with</span></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔵 Google", use_container_width=True, key="signin_google"):
                    st.info("🔄 Google OAuth coming soon!")
            with col2:
                if st.button("💼 LinkedIn", use_container_width=True, key="signin_linkedin"):
                    st.info("🔄 LinkedIn OAuth coming soon!")
            with col3:
                if st.button("Ⓜ️ Microsoft", use_container_width=True, key="signin_microsoft"):
                    st.info("🔄 Microsoft OAuth coming soon!")
        
        with tab2:
            # Sign Up Form
            st.markdown("### Create Your Account")
            
            with st.form("signup_form", clear_on_submit=False):
                name = st.text_input(
                    "Full Name",
                    placeholder="John Doe",
                    key="signup_name"
                )
                
                email = st.text_input(
                    "Email Address",
                    placeholder="your@email.com",
                    key="signup_email"
                )
                
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Min 6 characters",
                    key="signup_password",
                    help="Use a strong password with letters, numbers, and symbols"
                )
                
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter password",
                    key="signup_confirm"
                )
                
                agree_terms = st.checkbox(
                    "I agree to the Terms of Service and Privacy Policy",
                    key="agree_terms"
                )
                
                signup_submit = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")
                
                if signup_submit:
                    if not all([name, email, password, confirm_password]):
                        st.error("❌ Please fill in all fields")
                    elif len(password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    elif password != confirm_password:
                        st.error("❌ Passwords don't match")
                    elif not agree_terms:
                        st.error("❌ Please agree to Terms of Service")
                    else:
                        # Create account (in production, save to database)
                        if auth.login_with_email(email, password):  # Auto-login after signup
                            st.session_state.user_authenticated = True
                            st.session_state.user_email = email
                            st.session_state.user_name = name
                            st.session_state.show_auth_modal = False
                            st.success("✅ Account created successfully!")
                            st.balloons()
                            st.rerun()
            
            # OAuth options
            st.markdown('<div class="divider"><span>or sign up with</span></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔵 Google", use_container_width=True, key="signup_google"):
                    st.info("🔄 Google OAuth coming soon!")
            with col2:
                if st.button("💼 LinkedIn", use_container_width=True, key="signup_linkedin"):
                    st.info("🔄 LinkedIn OAuth coming soon!")
            with col3:
                if st.button("Ⓜ️ Microsoft", use_container_width=True, key="signup_microsoft"):
                    st.info("🔄 Microsoft OAuth coming soon!")
        
        # Guest mode option
        st.markdown("---")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.caption("No account needed? Continue as guest")
        with col2:
            if st.button("👤 Continue as Guest", use_container_width=True, key="guest_mode"):
                st.session_state.show_auth_modal = False
                st.info("✅ You can build resumes as a guest! Sign up later to save them.")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)


def show_user_profile():
    """Display user profile section"""
    auth = get_auth_manager()
    
    # Check if user is authenticated using legacy session state
    if not st.session_state.get('user_authenticated', False) and not auth.is_authenticated():
        return
    
    user_email = st.session_state.get('user_email', 'user@example.com')
    user_name = st.session_state.get('user_name', 'User')
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 Your Profile")
        
        # Profile card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;">👤</div>
            <div style="text-align: center;">
                <div style="font-weight: 600; font-size: 1.1rem;">{user_name}</div>
                <div style="font-size: 0.85rem; opacity: 0.9;">{user_email}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Account stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Resumes", st.session_state.get('saved_resumes_count', 0))
        with col2:
            st.metric("Templates", "29+")
        
        # Account actions
        if st.button("⚙️ Account Settings", use_container_width=True, key="account_settings"):
            st.info("Account settings coming soon!")
        
        if st.button("🚪 Sign Out", use_container_width=True, key="signout_btn"):
            auth.logout()
            st.session_state.user_authenticated = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.success("✅ Signed out successfully")
            st.rerun()


def show_auth_prompt_banner():
    """Show banner prompting users to sign up (for guest users)"""
    if st.session_state.user_authenticated:
        return
    
    st.info("""
    **👋 Hey there!** You're using SoulSkill as a guest. 
    **Sign up** to save your resumes and access them from any device! 
    """)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("✨ Sign Up Now", use_container_width=True, key="banner_signup"):
            st.session_state.show_auth_modal = True
            st.rerun()
