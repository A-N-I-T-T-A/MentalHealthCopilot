# app.py
import streamlit as st
from PIL import Image

from utils.db import init_db

from utils.quote_generator import get_daily_quote

# Initialize DB on app start
init_db()

st.set_page_config(
    page_title="Mental Health Copilot",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)




# --- Logo in Sidebar ---
try:
    logo = Image.open("assets/logo.png")
    st.sidebar.image(logo, width=100)
except:
    st.sidebar.write("🧠 Mental Health Copilot")  # Fallback if logo doesn't exist

# --- Professional Role-Based Sidebar ---
from utils.sidebar import show_sidebar
show_sidebar()

# --- Landing Page Content ---
with st.container():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🧠 Mental Health AI Copilot</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #555;'>Your companion for emotional wellbeing and self-care</h4>", unsafe_allow_html=True)

# --- Daily Quote Section ---
with st.container():
    st.markdown("<hr>", unsafe_allow_html=True)
    quote = get_daily_quote()
    st.markdown(f"<div style='background-color: #E8F5E9; padding: 20px; border-radius: 10px;'>"
                f"<h4 style='text-align: center; color: #2E7D32;'>{quote}</h4></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# --- Welcome Content ---
with st.container():
    if "user" not in st.session_state and "admin" not in st.session_state:
        st.warning("👈 Please use the sidebar to login or register first.")
    elif "user" in st.session_state:
        st.success(f"Welcome back, **{st.session_state['user']}!** Use the sidebar to explore features.", icon="👋")
    elif "admin" in st.session_state:
        st.success(f"Welcome, Admin **{st.session_state['admin']}!** Use the sidebar to access admin features.", icon="👋")

# Optional: Add footer or additional info
with st.container():
    st.markdown("<small style='text-align: center; color: #888;'>Take care of yourself, one step at a time.</small>", unsafe_allow_html=True)
