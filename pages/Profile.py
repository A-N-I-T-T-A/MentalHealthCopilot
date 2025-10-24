# pages/Profile.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.db import get_entries, get_entries_grouped_by_date, delete_user_and_entries, change_user_password
from utils.auth import require_login, clear_persistent_login
import hashlib

require_login()

# Show sidebar
from utils.sidebar import show_sidebar
show_sidebar()

# Page configuration
st.set_page_config(
    page_title="User Profile",
    page_icon="👤",
    layout="wide"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .profile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .profile-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .danger-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

user = st.session_state["user"]

# Profile Header
st.markdown(f"""
<div class="profile-header">
    <h1>👤 User Profile</h1>
    <h3 style="margin: 0.5rem 0 0 0; color: #f0f0f0;">{user}</h3>
    <p style="margin: 0.5rem 0 0 0; color: #f0f0f0;">Manage your account and view your activity</p>
</div>
""", unsafe_allow_html=True)

# Get user data
user_entries = get_entries(user)
user_activity = get_entries_grouped_by_date(user)

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Activity", "🔐 Security", "⚠️ Danger Zone"])

# Tab 1: Overview
with tab1:
    st.markdown("### 📊 Account Overview")
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="metric-value">{len(user_entries)}</div>
            <div class="metric-label">Total Entries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calculate days since first entry
        if user_entries:
            first_entry_date = min([datetime.fromisoformat(entry[5].replace(' ', 'T')) for entry in user_entries])
            days_active = (datetime.now() - first_entry_date).days + 1
        else:
            days_active = 0
        
        st.markdown(f"""
        <div class="stats-card">
            <div class="metric-value">{days_active}</div>
            <div class="metric-label">Days Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Calculate average entries per week
        if user_entries and days_active > 0:
            avg_per_week = (len(user_entries) / days_active) * 7
        else:
            avg_per_week = 0
        
        st.markdown(f"""
        <div class="stats-card">
            <div class="metric-value">{avg_per_week:.1f}</div>
            <div class="metric-label">Avg/Week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Calculate most common emotion
        if user_entries:
            emotions = [entry[3] for entry in user_entries]
            most_common = max(set(emotions), key=emotions.count)
        else:
            most_common = "None"
        
        st.markdown(f"""
        <div class="stats-card">
            <div class="metric-value">{most_common.title()}</div>
            <div class="metric-label">Top Emotion</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Account details
    st.markdown("### 📋 Account Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="profile-card">
            <h4>📧 Email Address</h4>
            <p style="font-size: 1.1rem; color: #495057;">{}</p>
        </div>
        """.format(user), unsafe_allow_html=True)
    
    with col2:
        # Calculate account age (approximate)
        if user_entries:
            account_age = days_active
        else:
            account_age = 1  # Default to 1 day if no entries
        
        st.markdown(f"""
        <div class="profile-card">
            <h4>📅 Account Age</h4>
            <p style="font-size: 1.1rem; color: #495057;">{account_age} days</p>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Activity
with tab2:
    st.markdown("### 📈 Your Activity")
    
    if user_entries:
        # Recent entries with delete functionality
        st.markdown("#### 📝 Recent Journal Entries")
        recent_entries = user_entries[:10]  # Show last 10 entries for better management
        
        for i, entry in enumerate(recent_entries):
            entry_id, user_email, entry_text, emotion, confidence, timestamp = entry
            entry_date = datetime.fromisoformat(timestamp.replace(' ', 'T'))
            
            # Create columns for entry display and delete button
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="profile-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>😊 {emotion.title()}</strong> - {entry_date.strftime('%B %d, %Y at %I:%M %p')}
                            <br><small style="color: #6c757d;">{entry_text[:100]}{'...' if len(entry_text) > 100 else ''}</small>
                        </div>
                        <div style="color: #28a745; font-weight: bold;">
                            {confidence:.2f}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🗑️", key=f"delete_entry_{entry_id}", help="Delete this entry"):
                    if st.session_state.get(f"confirm_delete_{entry_id}", False):
                        # Second confirmation - actually delete
                        from utils.db import delete_entry
                        delete_entry(entry_id)
                        st.success("✅ Entry deleted successfully!")
                        st.rerun()
                    else:
                        # First confirmation - set flag
                        st.session_state[f"confirm_delete_{entry_id}"] = True
                        st.warning("⚠️ Click again to confirm deletion")
            
            with col3:
                if st.session_state.get(f"confirm_delete_{entry_id}", False):
                    if st.button("❌", key=f"cancel_delete_{entry_id}", help="Cancel deletion"):
                        st.session_state[f"confirm_delete_{entry_id}"] = False
                        st.rerun()
            
            # Add some spacing between entries
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Activity chart
        st.markdown("#### 📊 Activity Over Time")
        if user_activity:
            df_activity = pd.DataFrame(user_activity, columns=['Date', 'Emotion', 'Count'])
            df_activity['Date'] = pd.to_datetime(df_activity['Date'])
            
            # Group by date and sum counts
            daily_activity = df_activity.groupby('Date')['Count'].sum().reset_index()
            
            import plotly.express as px
            fig = px.line(daily_activity, x='Date', y='Count', 
                         title="Daily Journal Entries",
                         color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 No journal entries found. Start journaling to see your activity here!")

# Tab 3: Security
with tab3:
    st.markdown("### 🔐 Security Settings")
    
    # Change Password Section
    st.markdown("""
    <div class="success-card">
        <h4>🔑 Change Password</h4>
        <p>Update your account password for better security.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password", help="Enter your current password")
        new_password = st.text_input("New Password", type="password", help="Enter your new password")
        confirm_password = st.text_input("Confirm New Password", type="password", help="Confirm your new password")
        
        submit_password = st.form_submit_button("🔑 Update Password", type="primary")
        
        if submit_password:
            if not all([current_password, new_password, confirm_password]):
                st.error("❌ Please fill in all password fields.")
            elif new_password != confirm_password:
                st.error("❌ New passwords do not match.")
            elif len(new_password) < 6:
                st.error("❌ Password must be at least 6 characters long.")
            else:
                # Verify current password and update
                success, message = change_user_password(user, current_password, new_password)
                if success:
                    st.success(f"✅ {message}")
                    # Clear the form fields after successful password change
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # Security Information
    st.markdown("""
    <div class="profile-card">
        <h4>🛡️ Security Information</h4>
        <ul>
            <li><strong>Account Status:</strong> Active ✅</li>
            <li><strong>Last Login:</strong> Current session</li>
            <li><strong>Password Strength:</strong> Good</li>
            <li><strong>Two-Factor Auth:</strong> Not enabled</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Tab 4: Danger Zone
with tab4:
    st.markdown("### ⚠️ Danger Zone")
    
    st.markdown("""
    <div class="danger-card">
        <h4>🗑️ Delete Account</h4>
        <p><strong>Warning:</strong> This action cannot be undone. This will permanently delete your account and all associated data including:</p>
        <ul>
            <li>All journal entries</li>
            <li>Emotion analysis data</li>
            <li>Account preferences</li>
            <li>Activity history</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Delete account form
    with st.form("delete_account_form"):
        st.warning("⚠️ **This action is permanent and cannot be undone!**")
        
        confirm_email = st.text_input("Type your email to confirm", placeholder="Enter your email address")
        confirm_text = st.text_input("Type 'DELETE MY ACCOUNT' to confirm", placeholder="DELETE MY ACCOUNT")
        
        submit_delete = st.form_submit_button("🗑️ Delete My Account", type="secondary")
        
        if submit_delete:
            if confirm_email != user:
                st.error("❌ Email does not match your account.")
            elif confirm_text != "DELETE MY ACCOUNT":
                st.error("❌ Please type 'DELETE MY ACCOUNT' exactly as shown.")
            else:
                # Implement actual account deletion
                st.warning("🚨 **FINAL WARNING**: This will permanently delete your account and all data!")
                
                # Add a second confirmation step
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ YES, DELETE MY ACCOUNT", type="primary", key="final_confirm_delete"):
                        if delete_user_and_entries(user):
                            st.success("✅ Account deleted successfully!")
                            clear_persistent_login()
                            st.switch_page("pages/Auth.py")
                        else:
                            st.error("❌ Failed to delete account. Please try again.")
                
                with col2:
                    if st.button("❌ CANCEL", key="cancel_delete"):
                        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <small>Mental Health AI Copilot - User Profile | 
    Last updated: {} | 
    User: {}</small>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user), unsafe_allow_html=True)
