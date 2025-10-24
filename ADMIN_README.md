# 📊 Admin Dashboard - Mental Health AI Copilot

## 🔐 Admin Access

### Default Admin Credentials
- **Email:** `admin@mentalhealth.com`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Change the default password after first login for security!

### Accessing the Dashboard
1. Go to the **Auth** page in your Streamlit app
2. Click on the **🔐 Admin Login** tab
3. Enter the admin credentials
4. You'll be redirected to the admin dashboard
5. The Admin Dashboard is hidden from regular users

## 🎯 Features Overview

### 📊 System Overview Tab
- **Key Metrics:** Total users, entries, average entries per user, database size
- **User Registration Trends:** Monthly registration charts
- **Journal Activity:** Daily activity trends over time
- **Real-time Statistics:** Live data from the database

### 👥 User Management Tab
- **User Statistics:** Total, active, and inactive user counts
- **User List:** Complete list of all registered users with status
- **User Export:** Download user data as CSV
- **User Status:** Active/Inactive indicators based on recent activity

### 📝 Journal Insights Tab
- **Entry Statistics:** Total entries, average confidence, weekly activity
- **Activity Trends:** Visual charts showing journal entry patterns
- **Date Filtering:** Filter data by custom date ranges
- **Engagement Metrics:** Track user engagement over time

### 😊 Emotion Analytics Tab
- **Emotion Distribution:** Pie charts showing overall emotion breakdown
- **Top Emotions:** Bar charts of most common emotions
- **Emotion Trends:** Line charts showing emotion patterns over time
- **Data Export:** Download emotion analysis data

### ⚙️ Admin Tools Tab
- **System Health:** Database size, total records, system status
- **User Management:** Delete users with confirmation prompts
- **Data Export:** Comprehensive data export functionality
- **System Monitoring:** Real-time system health indicators

## 🛠️ Technical Implementation

### Database Functions (utils/db.py)
- `create_admins_table()` - Creates admin authentication table
- `register_admin()` / `login_admin()` - Admin authentication
- `get_all_users()` - Retrieve all registered users
- `get_all_entries()` - Get journal entries (anonymized)
- `get_active_users()` - Users active in last 7 days
- `get_emotion_distribution()` - Emotion analytics
- `delete_user_and_entries()` - Safe user deletion
- `get_database_size()` - System health monitoring

### Authentication (utils/admin_auth.py)
- `require_admin()` - Access control for admin pages
- `admin_login_form()` - Beautiful login interface
- `admin_logout()` - Secure logout functionality

### Security Features
- **Separate Admin Authentication:** Independent from user system
- **Session Management:** Secure admin session handling
- **Access Control:** Admin-only page protection
- **Data Privacy:** No raw journal content exposed
- **Confirmation Dialogs:** Safe user deletion with confirmations

## 📈 Analytics & Reporting

### User Analytics
- Registration trends by month
- Active vs inactive user ratios
- User engagement metrics
- Geographic distribution (if available)

### Emotion Analytics
- Overall emotion distribution
- Emotion trends over time
- Confidence score analysis
- Seasonal emotion patterns

### System Analytics
- Database growth tracking
- Performance metrics
- Error monitoring
- Resource utilization

## 🔧 Admin Operations

### User Management
1. **View Users:** Complete user list with registration dates
2. **User Status:** Active/Inactive classification
3. **Delete Users:** Safe deletion with data cleanup
4. **Export Data:** CSV export of user information

### Data Export
- **User Data:** Email and registration dates
- **Emotion Data:** Aggregated emotion counts
- **Activity Data:** Journal entry patterns
- **Complete Reports:** Comprehensive system reports

### System Maintenance
- **Database Monitoring:** Size and health tracking
- **Performance Metrics:** System performance indicators
- **Data Cleanup:** Safe user and data removal
- **Backup Support:** Data export for backups

## 🎨 UI/UX Features

### Beautiful Design
- **Gradient Headers:** Modern, professional appearance
- **Metric Cards:** Clean, organized data presentation
- **Interactive Charts:** Plotly-powered visualizations
- **Responsive Layout:** Works on all screen sizes

### User Experience
- **Intuitive Navigation:** Tab-based organization
- **Real-time Updates:** Live data refresh
- **Date Filtering:** Flexible time range selection
- **Export Functionality:** Easy data download

### Accessibility
- **Clear Typography:** Readable fonts and sizes
- **Color Coding:** Status indicators and metrics
- **Confirmation Dialogs:** Safe operation confirmations
- **Error Handling:** Graceful error management

## 🚀 Getting Started

1. **Run Setup:** Execute `python setup_admin.py` (already done)
2. **Access Dashboard:** Go to Auth page → Admin Login tab
3. **Login:** Use default credentials (admin@mentalhealth.com / admin123)
4. **Change Password:** Update default password after first login
5. **Explore Features:** Navigate through all tabs in the admin dashboard

## 🔒 Security Best Practices

- Change default admin password immediately
- Use strong, unique passwords
- Monitor admin access logs
- Regular security updates
- Backup admin credentials securely

## 📞 Support

For technical support or questions about the admin dashboard:
- Check the database functions in `utils/db.py`
- Review authentication in `utils/admin_auth.py`
- Examine the main dashboard in `pages/Admin.py`

---

**Mental Health AI Copilot - Admin Dashboard**  
*Comprehensive system management and analytics platform*
