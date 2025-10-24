import streamlit as st
from utils.auth import clear_persistent_login

def show_logout():
    if "user" in st.session_state:
        st.sidebar.success(f"👋 Logged in as {st.session_state['user']}")
        if st.sidebar.button("🚪 Logout"):
            clear_persistent_login()  # Clear persistent login
            st.rerun()  # Refresh the page after logout
