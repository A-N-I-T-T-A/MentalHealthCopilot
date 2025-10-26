# 🧠 Mental Health AI Copilot

A comprehensive AI-powered mental health tracking and wellness platform built with Streamlit and BERT-based emotion classification.

## 🌟 Features

### 👤 User Features
- **Real-time Emotion Analysis** - BERT-based emotion detection
- **Mood Tracking** - Interactive mood calendar and trends
- **Wellness Tools** - Guided breathing exercises and self-care activities
- **Personalized Insights** - AI-powered recommendations and tips
- **Profile Management** - Account settings and data control

### 👨‍💼 Admin Features
- **System Analytics** - Comprehensive dashboard with charts and metrics
- **User Management** - Complete user administration and monitoring
- **Data Export** - CSV export with chart data for analysis
- **Real-time Monitoring** - System health and activity tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd MentalHealthCopilot
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv myvenv
   # Windows:
   myvenv\Scripts\activate
   # macOS/Linux:
   source myvenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your email credentials
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔐 Environment Setup

### Email Configuration
1. Copy `.env.example` to `.env`
2. Set up Gmail App Password:
   - Enable 2-Factor Authentication
   - Generate App Password in Google Account Settings
   - Use App Password in `.env` file

### Default Admin Access
- **Email**: admin@mentalhealth.com
- **Password**: admin123

⚠️ **Change admin password after first login!**

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python, SQLite
- **AI/ML**: BERT, Transformers, SHAP
- **Visualization**: Plotly, Matplotlib
- **Security**: SHA-256 hashing, Environment variables

## 📊 AI/ML Components

- **Emotion Classification**: DistilBERT-based model
- **Model Explainability**: SHAP for word-level impact analysis
- **Real-time Processing**: Instant emotion analysis
- **Confidence Scoring**: Emotion prediction confidence levels

## 📁 Project Structure

```
MentalHealthCopilot/
├── app.py                 # Main application
├── pages/                 # Streamlit pages
│   ├── Auth.py           # Authentication
│   ├── Home.py           # Emotion analysis
│   ├── Profile.py        # User profile
│   ├── History.py        # Mood tracking
│   ├── Admin.py          # Admin dashboard
│   └── WellnessTools.py  # Wellness activities
├── model/                 # AI/ML models
├── utils/                 # Utility functions
├── .env.example          # Environment template
├── requirements.txt      # Dependencies
└── SETUP.md             # Detailed setup guide
```

## 🔒 Security Features

- **Password Hashing**: SHA-256 encryption
- **Environment Variables**: Secure credential storage
- **Session Management**: Secure user sessions
- **Input Validation**: Comprehensive data validation
- **SQL Injection Prevention**: Parameterized queries

## 📈 Data Analytics

- **Mood Calendar**: Daily emotion tracking
- **Trend Analysis**: Weekly and monthly patterns
- **User Analytics**: Registration and activity trends
- **Emotion Distribution**: System-wide emotion analysis
- **Export Capabilities**: CSV export with chart data

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production
1. Set environment variables on hosting platform
2. Configure email credentials
3. Deploy using your preferred service

## 📝 License

This project is for educational and research purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions, please create an issue in the repository.

## 🔗 Links

- [Setup Guide](SETUP.md)
- [Admin Documentation](ADMIN_README.md)

---

**Built with ❤️ for mental health awareness and support**
