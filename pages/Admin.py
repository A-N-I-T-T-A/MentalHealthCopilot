# pages/Admin.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
from utils.db import (
    create_admins_table, get_all_users, get_all_entries, get_active_users,
    get_user_registrations_by_month, get_journal_activity_by_day,
    get_emotion_distribution, get_emotion_trends_by_week,
    delete_user_and_entries, get_database_size
)
from utils.admin_auth import require_admin
from utils.auth import clear_persistent_admin_login

# Check admin authentication
require_admin()

# Show sidebar
from utils.sidebar import show_sidebar
show_sidebar()

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .section-header {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #28a745;
    }
    .danger-button {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .success-button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Admin Dashboard</h1>
    <p>Mental Health AI Copilot - System Overview & Analytics</p>
    <p>Welcome, <strong>{}</strong> | <small>Last updated: {}</small></p>
</div>
""".format(st.session_state["admin"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Dashboard Controls")
    
    # Date range filter
    st.markdown("#### 📅 Date Range Filter")
    date_range = st.date_input(
        "Select date range:",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )
    
    # Admin actions
    st.markdown("#### ⚙️ Admin Actions")
    if st.button("🚪 Logout", use_container_width=True):
        clear_persistent_admin_login()
        st.success("👋 Admin logged out successfully!")
        st.switch_page("pages/Auth.py")

# Get data for the dashboard (used throughout the page)
all_users = get_all_users()
all_entries = get_all_entries()
active_users = get_active_users()

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", "👥 Users", "📝 Journal Insights", "😊 Emotion Analytics", "⚙️ Admin Tools"
])

# Tab 1: Overview
with tab1:
    st.markdown('<div class="section-header"><h3>📊 System Overview</h3></div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>👥 Total Users</h4>
            <h2 style="color: #667eea;">{}</h2>
        </div>
        """.format(len(all_users)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>📝 Total Entries</h4>
            <h2 style="color: #28a745;">{}</h2>
        </div>
        """.format(len(all_entries)), unsafe_allow_html=True)
    
    with col3:
        avg_entries = len(all_entries) / len(all_users) if all_users else 0
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Avg Entries/User</h4>
            <h2 style="color: #ffc107;">{:.1f}</h2>
        </div>
        """.format(avg_entries), unsafe_allow_html=True)
    
    with col4:
        db_size = get_database_size()
        st.markdown("""
        <div class="metric-card">
            <h4>💾 DB Size</h4>
            <h2 style="color: #dc3545;">{} MB</h2>
        </div>
        """.format(db_size), unsafe_allow_html=True)
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 User Registrations by Month")
        registrations = get_user_registrations_by_month()
        if registrations:
            df_reg = pd.DataFrame(registrations, columns=['Month', 'Count'])
            fig_reg = px.bar(df_reg, x='Month', y='Count', 
                           title="New User Registrations",
                           color='Count', color_continuous_scale='Blues')
            st.plotly_chart(fig_reg, use_container_width=True)
        else:
            st.info("No registration data available")
    
    with col2:
        st.markdown("#### 📊 Journal Activity (Last 30 Days)")
        activity = get_journal_activity_by_day()
        if activity:
            df_activity = pd.DataFrame(activity, columns=['Date', 'Count'])
            df_activity['Date'] = pd.to_datetime(df_activity['Date'])
            fig_activity = px.line(df_activity, x='Date', y='Count',
                                 title="Daily Journal Entries",
                                 color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig_activity, use_container_width=True)
        else:
            st.info("No activity data available")

# Tab 2: Users
with tab2:
    st.markdown('<div class="section-header"><h3>👥 User Management</h3></div>', unsafe_allow_html=True)
    
    # User statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Registered Users", len(all_users))
    
    with col2:
        st.metric("Active Users (7 days)", len(active_users))
    
    with col3:
        inactive_users = len(all_users) - len(active_users)
        st.metric("Inactive Users", inactive_users)
    
    # User list
    st.markdown("#### 📋 All Users")
    if all_users:
        df_users = pd.DataFrame(all_users, columns=['Email', 'Registration Date'])
        df_users['Registration Date'] = pd.to_datetime(df_users['Registration Date'])
        
        # Add user status
        df_users['Status'] = df_users['Email'].apply(
            lambda x: '🟢 Active' if x in active_users else '🔴 Inactive'
        )
        
        st.dataframe(df_users, use_container_width=True)
        
        # Export users
        # Format registration date for export
        df_users_export = df_users.copy()
        df_users_export['Registration Date'] = pd.to_datetime(df_users_export['Registration Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        csv_users = df_users_export.to_csv(index=False)
        st.download_button(
            label="📥 Download Users CSV",
            data=csv_users,
            file_name=f"users_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No users found")

# Tab 3: Journal Insights
with tab3:
    st.markdown('<div class="section-header"><h3>📝 Journal Insights</h3></div>', unsafe_allow_html=True)
    
    # Journal statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Journal Entries", len(all_entries))
    
    with col2:
        if all_entries:
            avg_confidence = sum(entry[2] for entry in all_entries) / len(all_entries)
            st.metric("Average Confidence", f"{avg_confidence:.2f}")
        else:
            st.metric("Average Confidence", "0.00")
    
    with col3:
        if all_entries:
            recent_entries = [e for e in all_entries if 
                            datetime.fromisoformat(e[3].replace(' ', 'T')) >= 
                            datetime.now() - timedelta(days=7)]
            st.metric("Entries This Week", len(recent_entries))
        else:
            st.metric("Entries This Week", 0)
    
    # Journal activity chart
    st.markdown("#### 📈 Journal Activity Trends")
    activity = get_journal_activity_by_day()
    if activity:
        df_activity = pd.DataFrame(activity, columns=['Date', 'Count'])
        df_activity['Date'] = pd.to_datetime(df_activity['Date'])
        
        # Filter by date range
        start_date, end_date = date_range
        df_activity = df_activity[
            (df_activity['Date'] >= pd.to_datetime(start_date)) &
            (df_activity['Date'] <= pd.to_datetime(end_date))
        ]
        
        fig_activity = px.area(df_activity, x='Date', y='Count',
                             title="Journal Entries Over Time",
                             color_discrete_sequence=['#28a745'])
        st.plotly_chart(fig_activity, use_container_width=True)
    else:
        st.info("No journal activity data available")

# Tab 4: Emotion Analytics
with tab4:
    st.markdown('<div class="section-header"><h3>😊 Emotion Analytics</h3></div>', unsafe_allow_html=True)
    
    # Emotion distribution
    emotions = get_emotion_distribution()
    if emotions:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥧 Emotion Distribution")
            df_emotions = pd.DataFrame(emotions, columns=['Emotion', 'Count'])
            fig_pie = px.pie(df_emotions, values='Count', names='Emotion',
                           title="Overall Emotion Distribution",
                           color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Top Emotions")
            fig_bar = px.bar(df_emotions.head(10), x='Count', y='Emotion',
                           orientation='h', title="Most Common Emotions",
                           color='Count', color_continuous_scale='Viridis')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Emotion trends
        st.markdown("#### 📈 Emotion Trends Over Time")
        trends = get_emotion_trends_by_week()
        if trends:
            df_trends = pd.DataFrame(trends, columns=['Week', 'Emotion', 'Count'])
            
            # Get top 5 emotions for trend analysis
            top_emotions = df_emotions.head(5)['Emotion'].tolist()
            df_trends_filtered = df_trends[df_trends['Emotion'].isin(top_emotions)]
            
            fig_trends = px.line(df_trends_filtered, x='Week', y='Count', color='Emotion',
                               title="Emotion Trends by Week",
                               color_discrete_sequence=px.colors.qualitative.Set1)
            st.plotly_chart(fig_trends, use_container_width=True)
        
        # Export emotion data
        csv_emotions = df_emotions.to_csv(index=False)
        st.download_button(
            label="📥 Download Emotion Data CSV",
            data=csv_emotions,
            file_name=f"emotion_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No emotion data available")

# Tab 5: Admin Tools
with tab5:
    st.markdown('<div class="section-header"><h3>⚙️ Admin Tools</h3></div>', unsafe_allow_html=True)
    
    # System Health
    st.markdown("#### 🏥 System Health")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Database Size", f"{get_database_size()} MB")
    
    with col2:
        st.metric("Total Records", len(all_entries) + len(all_users))
    
    with col3:
        st.metric("System Status", "🟢 Healthy")
    
    # User Management
    st.markdown("#### 👥 User Management")
    
    if all_users:
        # User selection for deletion
        user_emails = [user[0] for user in all_users]
        selected_user = st.selectbox("Select user to manage:", user_emails)
        
        if selected_user:
            # Show user info
            user_info = next(user for user in all_users if user[0] == selected_user)
            user_entries = [entry for entry in all_entries if entry[0] == selected_user]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"""
                **User Information:**
                - Email: {user_info[0]}
                - Registered: {user_info[1]}
                - Journal Entries: {len(user_entries)}
                - Status: {'🟢 Active' if selected_user in active_users else '🔴 Inactive'}
                """)
            
            with col2:
                st.warning("⚠️ **Danger Zone**")
                if st.button("🗑️ Delete User", type="secondary"):
                    st.session_state[f"confirm_delete_{selected_user}"] = True
                
                if st.session_state.get(f"confirm_delete_{selected_user}", False):
                    st.error(f"⚠️ Are you sure you want to delete user: **{selected_user}**?")
                    st.write("This will permanently delete:")
                    st.write("- User account")
                    st.write("- All journal entries")
                    st.write("- User preferences")
                    st.write("- Check-in responses")
                    
                    col_yes, col_no = st.columns(2)
                    
                    with col_yes:
                        if st.button("✅ Yes, Delete", type="primary"):
                            if delete_user_and_entries(selected_user):
                                st.success(f"✅ User {selected_user} deleted successfully!")
                                del st.session_state[f"confirm_delete_{selected_user}"]
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete user. Please try again.")
                    
                    with col_no:
                        if st.button("❌ Cancel"):
                            del st.session_state[f"confirm_delete_{selected_user}"]
                            st.rerun()
    
    # Export all data
    st.markdown("#### 📥 Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export All Data", use_container_width=True):
            # Create comprehensive report with proper column headers
            all_data_csv = ""
            
            # Users section
            if all_users:
                df_users = pd.DataFrame(all_users, columns=['Email', 'Registration Date'])
                # Format registration date properly
                df_users['Registration Date'] = pd.to_datetime(df_users['Registration Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
                all_data_csv += "\n=== USERS ===\n"
                all_data_csv += df_users.to_csv(index=False)
                all_data_csv += "\n"
            
            # Entries section
            if all_entries:
                df_entries = pd.DataFrame(all_entries, columns=['User', 'Emotion', 'Confidence', 'Timestamp'])
                # Format timestamp properly
                df_entries['Timestamp'] = pd.to_datetime(df_entries['Timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                all_data_csv += "\n=== ENTRIES ===\n"
                all_data_csv += df_entries.to_csv(index=False)
                all_data_csv += "\n"
            
            # Emotions section
            emotions = get_emotion_distribution()
            if emotions:
                df_emotions = pd.DataFrame(emotions, columns=['Emotion', 'Count'])
                all_data_csv += "\n=== EMOTIONS ===\n"
                all_data_csv += df_emotions.to_csv(index=False)
                all_data_csv += "\n"
            
            # Activity section
            activity = get_journal_activity_by_day()
            if activity:
                df_activity = pd.DataFrame(activity, columns=['Date', 'Entry Count'])
                # Format activity date properly
                df_activity['Date'] = pd.to_datetime(df_activity['Date']).dt.strftime('%Y-%m-%d')
                all_data_csv += "\n=== ACTIVITY ===\n"
                all_data_csv += df_activity.to_csv(index=False)
                all_data_csv += "\n"
            
            # Registrations section
            registrations = get_user_registrations_by_month()
            if registrations:
                df_registrations = pd.DataFrame(registrations, columns=['Month', 'Registration Count'])
                all_data_csv += "\n=== REGISTRATIONS ===\n"
                all_data_csv += df_registrations.to_csv(index=False)
                all_data_csv += "\n"
            
            st.download_button(
                label="📥 Download Complete Report",
                data=all_data_csv,
                file_name=f"admin_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <small>Mental Health AI Copilot - Admin Dashboard | 
    Last updated: {} | 
    Admin: {}</small>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), st.session_state["admin"]), unsafe_allow_html=True)
