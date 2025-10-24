# pages/Auth.py
import streamlit as st
import re
from utils.db import init_db, register_user, login_user, create_admins_table, login_admin
from utils.auth import set_persistent_login, clear_persistent_login, set_persistent_admin_login, clear_persistent_admin_login

# Validation functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def validate_form_data(email, password, confirm_password=None):
    """Validate all form data"""
    errors = []
    
    # Email validation
    if not email:
        errors.append("Email is required")
    elif not validate_email(email):
        errors.append("Please enter a valid email address")
    
    # Password validation
    if not password:
        errors.append("Password is required")
    else:
        is_valid, message = validate_password(password)
        if not is_valid:
            errors.append(message)
    
    # Confirm password validation (for registration)
    if confirm_password is not None:
        if not confirm_password:
            errors.append("Please confirm your password")
        elif password != confirm_password:
            errors.append("Passwords do not match")
    
    return errors

def validate_login_data(email, password):
    """Validate login form data - only check if fields are filled"""
    errors = []
    
    if not email:
        errors.append("Email is required")
    if not password:
        errors.append("Password is required")
    
    return errors

# --- Initialize database ---
init_db()
create_admins_table()  # Initialize admin table

# Show sidebar
from utils.sidebar import show_sidebar
show_sidebar()
# Page layout
st.set_page_config(page_title="Login/Register", page_icon="🔐", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔐 Welcome to Mental Health AI Copilot</h1>", unsafe_allow_html=True)


# --- Check if already logged in ---
if "user" in st.session_state:
    st.success(f"✅ Logged in as {st.session_state['user']}")
    
    st.markdown("### Navigate to:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home"):
            st.switch_page("pages/Home.py")
    with col2:
        if st.button("🌿 Wellness Tools"):
            st.switch_page("pages/WellnessTools.py")
    with col3:
        if st.button("📊 Mood Tracker"):
            st.switch_page("pages/MoodTracker.py")

elif "admin" in st.session_state:
    st.success(f"✅ Admin logged in as {st.session_state['admin']}")
    
    st.markdown("### Admin Dashboard:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Admin Dashboard", type="primary"):
            st.switch_page("pages/Admin.py")
    with col2:
        if st.button("🚪 Admin Logout"):
            clear_persistent_admin_login()
            st.rerun()
    
else:
    # --- Create tabs for different login types ---
    tab1, tab2, tab3 = st.tabs(["👤 User Login", "🆕 User Register", "🔐 Admin Login"])
    
    # Tab 1: User Login
    with tab1:
        st.subheader("👤 Login to Your Account")
        st.markdown("<p style='text-align: center; color: gray;'>Please login to track your mood and emotions.</p>", unsafe_allow_html=True)
        
        with st.form("user_login_form"):
            email = st.text_input("📧 Email", placeholder="user@example.com", help="Enter your registered email address")
            password = st.text_input("🔑 Password", type="password", help="Enter your password")
            submit = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
            
            if submit:
                # Validate login data - only check if fields are filled
                errors = validate_login_data(email, password)
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Attempt login
                    user = login_user(email, password)
                    if user:
                        set_persistent_login(email)  # Set persistent login
                        st.success(f"✅ Welcome back, {email}!")
                        st.switch_page("pages/Home.py")
                    else:
                        st.error("❌ Invalid email or password. Please check your credentials and try again.")
        
        st.markdown("[Forgot Password?](#)", unsafe_allow_html=True)
    
    # Tab 2: User Registration
    with tab2:
        st.subheader("🆕 Create a New Account")
        st.markdown("<p style='text-align: center; color: gray;'>Join our community to start tracking your mental wellness.</p>", unsafe_allow_html=True)
        
        with st.form("user_register_form"):
            email = st.text_input("📧 Email", placeholder="user@example.com", help="Enter a valid email address")
            password = st.text_input("🔑 Password", type="password", help="Password must be at least 6 characters with letters and numbers")
            confirm_password = st.text_input("🔑 Confirm Password", type="password", help="Re-enter your password to confirm")
            
            # Password requirements display
            st.markdown("""
            <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #007bff;">
                <h6 style="margin: 0 0 5px 0; color: #495057;">🔒 Password Requirements:</h6>
                <ul style="margin: 0; padding-left: 20px; color: #6c757d; font-size: 0.9rem;">
                    <li>At least 6 characters long</li>
                    <li>Contains at least one letter</li>
                    <li>Contains at least one number</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            submit = st.form_submit_button("✨ Register", type="primary", use_container_width=True)
            
            if submit:
                # Validate form data
                errors = validate_form_data(email, password, confirm_password)
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Attempt registration
                    if register_user(email, password):
                        st.success("✅ Registration successful! You can now login.")
                        st.switch_page("pages/Auth.py")
                    else:
                        st.error("⚠️ Email already exists. Please try a different email address.")
    
    # Tab 3: Admin Login
    with tab3:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0;">🔐 Admin Access</h3>
            <p style="color: #f0f0f0; margin: 10px 0 0 0;">System administrators only</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            email = st.text_input("📧 Admin Email", placeholder="admin@example.com", help="Enter your admin email address")
            password = st.text_input("🔑 Admin Password", type="password", help="Enter your admin password")
            submit = st.form_submit_button("🚀 Admin Login", type="primary", use_container_width=True)
            
            if submit:
                # Validate login data - only check if fields are filled
                errors = validate_login_data(email, password)
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Attempt admin login
                    admin = login_admin(email, password)
                    if admin:
                        set_persistent_admin_login(email)
                        st.success(f"✅ Admin login successful! Welcome, {email}")
                        st.switch_page("pages/Admin.py")
                    else:
                        st.error("❌ Invalid admin credentials. Please check your email and password.")
        
        st.info("💡 **Default Admin Credentials:** admin@mentalhealth.com / admin123")
