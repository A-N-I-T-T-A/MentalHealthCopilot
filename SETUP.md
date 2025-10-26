# 🚀 Mental Health AI Copilot - Setup Guide

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git (for version control)

## 🔧 Installation Steps

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd MentalHealthCopilot
```

### 2. Create Virtual Environment
```bash
python -m venv myvenv

# On Windows:
myvenv\Scripts\activate

# On macOS/Linux:
source myvenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

#### Create Environment File
```bash
# Copy the example environment file
cp .env.example .env
```

#### Configure Email Settings
Edit the `.env` file with your email credentials:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
```

#### Gmail App Password Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings > Security > App passwords
3. Generate an app password for "Mail"
4. Use this app password in the `.env` file (not your regular password)

### 5. Initialize Database
The database will be created automatically on first run.

### 6. Run the Application
```bash
streamlit run app.py
```

## 🔐 Security Notes

- **Never commit the `.env` file** to version control
- **Use App Passwords** for Gmail instead of regular passwords
- **Keep your credentials secure** and don't share them

## 📁 Project Structure

```
MentalHealthCopilot/
├── app.py                 # Main application entry point
├── pages/                 # Streamlit pages
│   ├── Auth.py           # Authentication
│   ├── Home.py           # Emotion analysis
│   ├── Profile.py        # User profile
│   ├── History.py        # Mood tracking
│   ├── Admin.py          # Admin dashboard
│   └── WellnessTools.py  # Wellness activities
├── model/                 # AI/ML models
│   └── emotion_classifier.py
├── utils/                 # Utility functions
│   ├── db.py             # Database operations
│   ├── auth.py           # Authentication
│   ├── email_utils.py    # Email services
│   └── ...
├── .env.example          # Environment template
├── .env                  # Your environment config (not in git)
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🎯 Default Admin Access

- **Email**: admin@mentalhealth.com
- **Password**: admin123

⚠️ **Change the admin password after first login!**

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. Set up environment variables on your hosting platform
2. Configure email credentials
3. Deploy using your preferred hosting service (Heroku, AWS, etc.)

## 🆘 Troubleshooting

### Email Not Working
- Check if `.env` file exists and has correct credentials
- Verify Gmail App Password is correct
- Ensure 2FA is enabled on Gmail account

### Database Issues
- Delete `mental_health.db` to reset database
- Check file permissions

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

## 📞 Support

For issues and questions, please create an issue in the repository.
