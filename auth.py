"""
Authentication & Security for SoulSkill Resume Builder
Supports OAuth (Google, LinkedIn, Microsoft) and secure data handling
"""
import os
import hashlib
import secrets
from typing import Optional, Dict
import streamlit as st

# OAuth Configuration
OAUTH_CONFIG = {
    'google': {
        'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
        'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8502/oauth/callback'),
        'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'scopes': ['email', 'profile']
    },
    'linkedin': {
        'client_id': os.getenv('LINKEDIN_CLIENT_ID', ''),
        'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET', ''),
        'redirect_uri': os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8502/oauth/callback'),
        'auth_url': 'https://www.linkedin.com/oauth/v2/authorization',
        'token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
        'scopes': ['r_liteprofile', 'r_emailaddress']
    },
    'microsoft': {
        'client_id': os.getenv('MICROSOFT_CLIENT_ID', ''),
        'client_secret': os.getenv('MICROSOFT_CLIENT_SECRET', ''),
        'redirect_uri': os.getenv('MICROSOFT_REDIRECT_URI', 'http://localhost:8502/oauth/callback'),
        'auth_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
        'token_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        'scopes': ['User.Read']
    }
}

class AuthManager:
    """Manage user authentication and sessions"""
    
    def __init__(self):
        self.session_key = 'soulskill_auth'
        self._init_session()
    
    def _init_session(self):
        """Initialize authentication session state"""
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                'is_authenticated': False,
                'user': None,
                'session_token': None
            }
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        self._init_session()  # Ensure session is initialized
        return st.session_state[self.session_key]['is_authenticated']
    
    def get_current_user(self) -> Optional[Dict]:
        """Get currently authenticated user"""
        if self.is_authenticated():
            return st.session_state[self.session_key]['user']
        return None
    
    def login_with_email(self, email: str, password: str) -> bool:
        """Simple email/password login (demo mode)"""
        # In production, verify against database with hashed passwords
        hashed_password = self._hash_password(password)
        
        # TODO: Verify against database
        # For now, just accept any email
        if email and len(password) >= 6:
            st.session_state[self.session_key] = {
                'is_authenticated': True,
                'user': {
                    'email': email,
                    'name': email.split('@')[0],
                    'provider': 'email'
                },
                'session_token': secrets.token_urlsafe(32)
            }
            return True
        return False
    
    def login_with_oauth(self, provider: str):
        """Initiate OAuth login flow"""
        if provider not in OAUTH_CONFIG:
            st.error(f"❌ OAuth provider '{provider}' not configured")
            return
        
        config = OAUTH_CONFIG[provider]
        
        if not config['client_id']:
            st.warning(f"⚠️ {provider.title()} OAuth not configured. Set environment variables.")
            return
        
        # Generate state token for CSRF protection
        state = secrets.token_urlsafe(32)
        st.session_state['oauth_state'] = state
        
        # Build authorization URL
        scopes = ' '.join(config['scopes'])
        auth_url = (
            f"{config['auth_url']}?"
            f"client_id={config['client_id']}&"
            f"redirect_uri={config['redirect_uri']}&"
            f"response_type=code&"
            f"scope={scopes}&"
            f"state={state}"
        )
        
        st.info(f"🔐 Redirecting to {provider.title()} login...")
        st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)
    
    def logout(self):
        """Logout current user"""
        st.session_state[self.session_key] = {
            'is_authenticated': False,
            'user': None,
            'session_token': None
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = os.getenv('PASSWORD_SALT', 'soulskill_default_salt')
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def require_auth(self):
        """Decorator/middleware to require authentication"""
        if not self.is_authenticated():
            self.show_login_page()
            st.stop()
    
    def show_login_page(self):
        """Display login UI"""
        st.markdown("## 🔐 Login to SoulSkill")
        st.caption("Sign in to save and manage your resumes")
        
        tab1, tab2 = st.tabs(["Email Login", "OAuth Login"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="Min 6 characters")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Login", use_container_width=True)
                with col2:
                    if st.form_submit_button("Continue as Guest", use_container_width=True):
                        # Skip login, use anonymous mode
                        st.session_state[self.session_key]['is_authenticated'] = False
                        st.rerun()
                
                if submit:
                    if self.login_with_email(email, password):
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Password must be at least 6 characters.")
        
        with tab2:
            st.caption("Sign in with your existing account:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔵 Google", use_container_width=True, key="google_login"):
                    self.login_with_oauth('google')
            
            with col2:
                if st.button("💼 LinkedIn", use_container_width=True, key="linkedin_login"):
                    self.login_with_oauth('linkedin')
            
            with col3:
                if st.button("Ⓜ️ Microsoft", use_container_width=True, key="microsoft_login"):
                    self.login_with_oauth('microsoft')
            
            st.info("💡 **Note**: OAuth requires configuration. Set environment variables or continue as guest.")


class SecurityManager:
    """Handle security and data protection"""
    
    @staticmethod
    def encrypt_sensitive_data(data: str) -> str:
        """Encrypt sensitive data (placeholder - use proper encryption in production)"""
        # In production, use cryptography library with Fernet encryption
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS"""
        # Basic sanitization - in production use bleach or similar library
        dangerous_chars = ['<', '>', '"', "'", '&']
        for char in dangerous_chars:
            text = text.replace(char, '')
        return text
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate CSRF token for form protection"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_csrf_token(token: str) -> bool:
        """Validate CSRF token"""
        expected = st.session_state.get('csrf_token')
        return token == expected


# Global auth instance
auth_manager = None

def get_auth_manager() -> AuthManager:
    """Get or create auth manager singleton"""
    global auth_manager
    if auth_manager is None:
        auth_manager = AuthManager()
    return auth_manager


def show_auth_sidebar():
    """Show authentication status in sidebar"""
    auth = get_auth_manager()
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 Account")
        
        if auth.is_authenticated():
            user = auth.get_current_user()
            st.success(f"✅ Logged in as {user['name']}")
            st.caption(f"📧 {user['email']}")
            
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                auth.logout()
                st.success("✅ Logged out successfully")
                st.rerun()
        else:
            st.info("👋 Not logged in (Guest mode)")
            if st.button("🔐 Login", use_container_width=True, key="sidebar_login_btn"):
                st.session_state['show_login'] = True
                st.rerun()
