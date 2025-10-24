# utils/auth.py
import streamlit as st
from utils.db import register_user, login_user
import os
import json
from datetime import datetime, timedelta

SESSION_FILE = "user_session.json"

def save_session(email):
    """Save user session to file."""
    session_data = {
        "user": email,
        "timestamp": datetime.now().isoformat()
    }
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)
    except Exception:
        pass  # If file write fails, continue without persistence

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

def clear_session():
    """Clear user session file."""
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception:
        pass  # If file delete fails, continue

def require_login():
    """Redirect users to login if not authenticated."""
    # Check if user is in session state
    if "user" not in st.session_state:
        # Try to restore from session file
        saved_user = load_session()
        if saved_user:
            st.session_state["user"] = saved_user
            return
    
    # If still not authenticated, show login message
    if "user" not in st.session_state:
        st.warning("🔒 Please login to access this feature.")
        st.stop()  # Stop execution if user not logged in

def set_persistent_login(email):
    """Set persistent login using file storage."""
    st.session_state["user"] = email
    save_session(email)

def set_persistent_admin_login(email):
    """Set persistent admin login using file storage."""
    st.session_state["admin"] = email
    save_session(f"admin_{email}")

def clear_persistent_login():
    """Clear persistent login on logout."""
    if "user" in st.session_state:
        del st.session_state["user"]
    clear_session()

def clear_persistent_admin_login():
    """Clear persistent admin login on logout."""
    if "admin" in st.session_state:
        del st.session_state["admin"]
    clear_session()
