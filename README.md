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


## 📈 Data Analytics

- **Mood Calendar**: Daily emotion tracking
- **Trend Analysis**: Weekly and monthly patterns
- **User Analytics**: Registration and activity trends
- **Emotion Distribution**: System-wide emotion analysis
- **Export Capabilities**: CSV export with chart data

