# utils/admin_auth.py
import streamlit as st
import os
import json
from datetime import datetime, timedelta

SESSION_FILE = "user_session.json"

def load_session():
    """Load user session from file."""
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                session_data = json.load(f)
            
            # Check if session is not too old (24 hours)
            session_time = datetime.fromisoformat(session_data["timestamp"])
            if datetime.now() - session_time < timedelta(hours=24):
                return session_data["user"]
    except Exception:
        pass  # If file read fails, return None
    
    return None

def require_admin():
    """Require admin authentication to access admin pages."""
    # Check if admin is in session state
    if "admin" not in st.session_state:
        # Try to restore from session file
        saved_user = load_session()
        if saved_user and saved_user.startswith("admin_"):
            # Extract admin email from saved session
            admin_email = saved_user.replace("admin_", "")
            st.session_state["admin"] = admin_email
            return
    
    # If still not authenticated, show login message
    if "admin" not in st.session_state:
        st.error("🚫 **Access Denied** - Admin privileges required")
        st.info("Please login as an admin to access this page.")
        st.markdown("### 🔐 Admin Login Required")
        st.markdown("To access the admin dashboard, please:")
        st.markdown("1. Go to the **Auth** page")
        st.markdown("2. Click on the **🔐 Admin Login** tab")
        st.markdown("3. Enter your admin credentials")
        
        if st.button("🔐 Go to Admin Login", type="primary"):
            st.switch_page("pages/Auth.py")
        st.stop()
