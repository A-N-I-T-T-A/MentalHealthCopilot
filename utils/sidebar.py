# utils/sidebar.py
import streamlit as st
from utils.auth import clear_persistent_login, clear_persistent_admin_login

def show_sidebar():
    """Show the professional role-based sidebar."""
    
    # Hide default Streamlit navigation and show custom sidebar
    st.markdown("""
    <style>
        /* Hide default Streamlit navigation completely */
        section[data-testid="stSidebar"] > div:first-child > div:first-child {
            display: none !important;
        }
        
        /* Hide page navigation links */
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {
            display: none !important;
        }
        
        /* Hide navigation elements */
        .stSidebar .stSelectbox, .stSidebar nav {
            display: none !important;
        }
        
        /* Hide any remaining navigation elements */
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Hide sidebar navigation container */
        .css-1d391kg {
            display: none !important;
        }
        
        /* More aggressive hiding */
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Hide any auto-generated navigation */
        .stSidebar .stSelectbox {
            display: none !important;
        }
        
        /* Custom sidebar styling */
        .sidebar-user-info {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 0.5rem 0.8rem;
            border-radius: 6px;
            margin-bottom: 0.8rem;
            color: #495057;
            text-align: center;
            font-size: 0.8rem;
            border: 1px solid #dee2e6;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .sidebar-admin-info {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            padding: 0.5rem 0.8rem;
            border-radius: 6px;
            margin-bottom: 0.8rem;
            color: #856404;
            text-align: center;
            font-size: 0.8rem;
            border: 1px solid #ffeaa7;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .nav-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        .nav-section-admin {
            background: #fff5f5;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid #ff6b6b;
        }
        .section-title {
            font-weight: bold;
            color: #495057;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
    
    <script>
    // Additional JavaScript to hide default navigation
    function hideDefaultNav() {
        // Hide any remaining navigation elements
        const navElements = document.querySelectorAll('[data-testid="stSidebarNav"], .stSidebar nav, .stSidebar .stSelectbox');
        navElements.forEach(el => {
            if (el) el.style.display = 'none';
        });
        
        // Hide the first child of sidebar (usually the navigation)
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar && sidebar.firstElementChild) {
            sidebar.firstElementChild.style.display = 'none';
        }
        
        // Hide any page navigation links
        const pageLinks = document.querySelectorAll('a[data-testid="stSidebarNavLink"]');
        pageLinks.forEach(link => {
            if (link) link.style.display = 'none';
        });
    }
    
    // Run immediately and on page changes
    hideDefaultNav();
    setTimeout(hideDefaultNav, 100);
    setTimeout(hideDefaultNav, 500);
    
    // Also run when the page changes
    window.addEventListener('load', hideDefaultNav);
    </script>
    """, unsafe_allow_html=True)

    # --- User Info Section ---
    if "user" in st.session_state:
        st.markdown(f"""
        <div class="sidebar-user-info">
            <h5 style="margin: 0; color: #495057; font-size: 0.9rem; font-weight: 600;">👤 {st.session_state['user']}</h5>
            <p style="margin: 0.2rem 0 0 0; color: #6c757d; font-size: 0.7rem;">Regular User</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User Navigation
        st.sidebar.markdown('<div class="nav-section"><div class="section-title">🧭 User Navigation</div></div>', unsafe_allow_html=True)
        
        if st.sidebar.button("🏠 Home", use_container_width=True, key="user_home"):
            st.switch_page("app.py")
        
        if st.sidebar.button("📝 Journal Entry", use_container_width=True, key="user_journal"):
            st.switch_page("pages/Home.py")
        
        if st.sidebar.button("🌿 Wellness Tools", use_container_width=True, key="user_wellness"):
            st.switch_page("pages/WellnessTools.py")
        
        if st.sidebar.button("📈 Trends", use_container_width=True, key="user_trends"):
            st.switch_page("pages/Trends.py")
        
        if st.sidebar.button("📖 Journal History", use_container_width=True, key="user_history"):
            st.switch_page("pages/History.py")
        
        # Dedicated account section for users
        st.sidebar.markdown('<div class="nav-section"><div class="section-title">🚪 Account</div></div>', unsafe_allow_html=True)
        if st.sidebar.button("👤 Profile", use_container_width=True, key="user_profile"):
            st.switch_page("pages/Profile.py")
        if st.sidebar.button("🚪 Logout", use_container_width=True, key="user_logout_main"):
            clear_persistent_login()
            st.switch_page("app.py")

    elif "admin" in st.session_state:
        st.markdown(f"""
        <div class="sidebar-admin-info">
            <h5 style="margin: 0; color: #856404; font-size: 0.9rem; font-weight: 600;">🔐 {st.session_state['admin']}</h5>
            <p style="margin: 0.2rem 0 0 0; color: #b8860b; font-size: 0.7rem;">System Administrator</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Admin Navigation
        st.sidebar.markdown('<div class="nav-section-admin"><div class="section-title">⚙️ Admin Panel</div></div>', unsafe_allow_html=True)
        
        if st.sidebar.button("📊 Dashboard", use_container_width=True, key="admin_dashboard"):
            st.switch_page("pages/Admin.py")
        
        # Admin Quick Stats
        st.sidebar.markdown('<div class="nav-section-admin"><div class="section-title">📊 Quick Stats</div></div>', unsafe_allow_html=True)
        
        try:
            from utils.db import get_all_users, get_all_entries, get_active_users
            all_users = get_all_users()
            all_entries = get_all_entries()
            active_users = get_active_users()
            
            st.sidebar.metric("👥 Total Users", len(all_users))
            st.sidebar.metric("📝 Total Entries", len(all_entries))
            st.sidebar.metric("🟢 Active Users", len(active_users))
        except:
            st.sidebar.info("📊 Stats unavailable")
        
        # Dedicated logout section for admins
        st.sidebar.markdown('<div class="nav-section-admin"><div class="section-title">🚪 Account</div></div>', unsafe_allow_html=True)
        if st.sidebar.button("🚪 Logout", use_container_width=True, key="admin_logout_main"):
            clear_persistent_admin_login()
            st.rerun()

    else:
        # Not logged in
        st.markdown("""
        <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                    padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;
                    color: white; text-align: center;">
            <h4 style="margin: 0; color: white;">🔐 Welcome</h4>
            <p style="margin: 0.5rem 0 0 0; color: #f0f0f0; font-size: 0.9rem;">Please login to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown('<div class="nav-section"><div class="section-title">🔑 Authentication</div></div>', unsafe_allow_html=True)
        
        if st.sidebar.button("🔑 Login / Register", use_container_width=True, type="primary", key="auth_btn"):
            st.switch_page("pages/Auth.py")
        
        st.sidebar.markdown("---")
        st.sidebar.info("👈 Use the login button to access your account or admin panel")
