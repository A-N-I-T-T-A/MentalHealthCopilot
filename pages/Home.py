# pages/Home.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from model.emotion_classifier import model_loader
from utils.shap_explainer import explain_text
from utils.tokenizer_utils import clean_bert_tokens
from utils.db import add_entry, add_checkin, create_checkins_table, create_preferences_table
from utils.auth import require_login

import torch
import shap
import nltk
import math
from nltk.corpus import stopwords


# Initialize
require_login()
create_checkins_table()
create_preferences_table()

# Show sidebar
from utils.sidebar import show_sidebar
show_sidebar()

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

tokenizer = model_loader.tokenizer

st.title("🧠 Emotion Insight")
st.markdown("Enter your thoughts or journal entry below to get emotional insights.")

user_input = st.text_area("💬 Your Journal Entry", height=200)

if st.button("🧾 Analyze Emotion"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            top_emotions, logits = model_loader.predict_emotion(user_input)

            filtered_emotions = [(label, score) for label, score in top_emotions if score > 0.5][:2]
            st.subheader("🧠 Detected Emotions")
            if filtered_emotions:
                for label, score in filtered_emotions:
                    st.write(f"**{label.title()}** – Confidence: `{score:.2f}`")
            else:
                st.info("No strong emotions detected with confidence > 0.5.")

            if filtered_emotions:
                primary_emotion, confidence = filtered_emotions[0]
                add_entry(st.session_state["user"], user_input, primary_emotion, confidence)
                st.success("✅ Your entry has been saved to your journal.")

                # Show wellness tools link
                st.subheader("🌿 Wellness Tools")
                st.markdown(
                    "Explore guided breathing, mood reflection, and self-care activities in the **Wellness Tools** section."
                )
                st.page_link("pages/WellnessTools.py", label="👉 Go to Wellness Tools")
            # Enhanced SHAP Explanation with Visual Elements
            st.subheader("📊 Why These Emotions?")
            shap_values = explain_text(user_input)
            shap_labels = [label.strip().lower() for label in shap_values.output_names]

            explainable_emotion, emotion_index = None, None
            for label, _ in filtered_emotions:
                if label.lower() in shap_labels:
                    explainable_emotion = label
                    emotion_index = shap_labels.index(label.lower())
                    break

            if explainable_emotion is None:
                st.warning("SHAP explanation is not available for the detected emotions.")
            else:
                input_ids = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)["input_ids"][0]
                shap_tokens = tokenizer.convert_ids_to_tokens(input_ids)
                cleaned_tokens = clean_bert_tokens(shap_tokens)
                shap_scores = shap_values[0].values[emotion_index]

                # Get important words with their scores
                word_scores = []
                for i, score in enumerate(shap_scores):
                    if i < len(cleaned_tokens):
                        word = cleaned_tokens[i].lower()
                        if word not in stop_words and word.isalpha() and len(word) > 2:
                            word_scores.append((cleaned_tokens[i], abs(score), score))
                
                # Sort by importance (absolute score)
                word_scores.sort(key=lambda x: x[1], reverse=True)
                top_words = word_scores[:8]  # Get top 8 words
                
                if top_words:
                    # Create two columns for better layout
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Create word cloud visualization using Streamlit components
                        st.markdown("#### 🎨 Word Impact Visualization")
                        
                        # Create a container for the word cloud
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                                    padding: 20px; border-radius: 15px; margin: 10px 0;
                                    border: 1px solid #dee2e6; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <h4 style="text-align: center; color: #495057; margin-bottom: 15px;">
                                💡 Key Words Influencing <span style="color: #667eea;">{}</span>
                            </h4>
                        """.format(explainable_emotion.title()), unsafe_allow_html=True)
                        
                        # Create word cloud using Streamlit columns and metrics
                        word_cols = st.columns(len(top_words))
                        
                        for i, (word, abs_score, score) in enumerate(top_words):
                            with word_cols[i]:
                                # Determine color and styling based on impact
                                if score > 0:
                                    # Positive impact - green
                                    st.markdown(f"""
                                    <div style="background: #28a745; color: white; padding: 10px; 
                                                border-radius: 15px; text-align: center; margin: 5px;
                                                box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                                        <strong>{word}</strong>
                                        <br><small>+{score:.3f}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    # Negative impact - red
                                    st.markdown(f"""
                                    <div style="background: #dc3545; color: white; padding: 10px; 
                                                border-radius: 15px; text-align: center; margin: 5px;
                                                box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                                        <strong>{word}</strong>
                                        <br><small>{score:.3f}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Add legend
                        st.markdown("""
                        <div style="text-align: center; margin-top: 15px; font-size: 0.9rem; color: #6c757d;">
                            <span style="color: #28a745;">●</span> Positive Impact &nbsp;&nbsp;
                            <span style="color: #dc3545;">●</span> Negative Impact
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add emotion insights card directly under word visualization
                        st.markdown("#### 💡 Emotion Insights")
                        
                        # Get the primary emotion from filtered_emotions
                        primary_emotion = filtered_emotions[0][0].lower() if filtered_emotions else 'neutral'
                        
                        # Emotion-specific insights
                        emotion_insights = {
                            'happy': {
                                'icon': '😊',
                                'message': 'Great! You\'re feeling positive. This is a wonderful state to be in.',
                                'tips': ['Share your joy with others', 'Practice gratitude', 'Engage in activities you love'],
                                'color': '#28a745'
                            },
                            'sad': {
                                'icon': '😢',
                                'message': 'It\'s okay to feel sad. This is a natural human emotion.',
                                'tips': ['Allow yourself to feel', 'Reach out to loved ones', 'Practice self-compassion'],
                                'color': '#6f42c1'
                            },
                            'angry': {
                                'icon': '😠',
                                'message': 'Anger is a valid emotion. Let\'s channel it constructively.',
                                'tips': ['Take deep breaths', 'Identify the source', 'Express feelings calmly'],
                                'color': '#dc3545'
                            },
                            'fear': {
                                'icon': '😰',
                                'message': 'Fear can be overwhelming, but you\'re stronger than you think.',
                                'tips': ['Focus on what you can control', 'Practice mindfulness', 'Seek support if needed'],
                                'color': '#fd7e14'
                            },
                            'surprise': {
                                'icon': '😲',
                                'message': 'Surprise can be exciting or unsettling. How are you feeling about it?',
                                'tips': ['Take time to process', 'Embrace the unexpected', 'Stay open to new experiences'],
                                'color': '#20c997'
                            },
                            'disgust': {
                                'icon': '🤢',
                                'message': 'Disgust is a protective emotion. What\'s causing this feeling?',
                                'tips': ['Identify the trigger', 'Create distance if needed', 'Focus on what feels good'],
                                'color': '#6c757d'
                            },
                            'neutral': {
                                'icon': '😐',
                                'message': 'Neutral is a balanced state. You\'re in a calm, centered place.',
                                'tips': ['Enjoy the peace', 'Practice mindfulness', 'Use this time for reflection'],
                                'color': '#17a2b8'
                            }
                        }
                        
                        insight = emotion_insights.get(primary_emotion, emotion_insights['neutral'])
                        
                        st.markdown(f"""
                        <div style="background: {insight['color']}; color: white; padding: 15px; 
                                    border-radius: 10px; margin: 10px 0; text-align: center;">
                            <h4 style="margin: 0 0 10px 0;">{insight['icon']} {primary_emotion.title()}</h4>
                            <p style="margin: 0 0 10px 0; font-size: 1rem;">{insight['message']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add wellness tools link
                        st.markdown("#### 🌿 Wellness Tools")
                        st.markdown(
                            "Explore guided breathing, mood reflection, and self-care activities in the **Wellness Tools** section."
                        )
                        st.page_link("pages/WellnessTools.py", label="👉 Go to Wellness Tools")
                    
                    with col2:
                        # Create impact score chart
                        st.markdown("#### 📈 Word Impact Scores")
                        
                        # Prepare data for the chart
                        chart_data = []
                        for word, abs_score, score in top_words[:5]:  # Top 5 for chart
                            chart_data.append({
                                'Word': word,
                                'Impact': abs_score,
                                'Type': 'Positive' if score > 0 else 'Negative'
                            })
                        
                        if chart_data:
                            chart_df = pd.DataFrame(chart_data)
                            fig = px.bar(chart_df, x='Impact', y='Word', 
                                        color='Type', orientation='h',
                                        color_discrete_map={'Positive': '#28a745', 'Negative': '#dc3545'},
                                        title="Word Impact Scores")
                            fig.update_layout(height=300, showlegend=True)
                            st.plotly_chart(fig, use_container_width=True)
                        
                else:
                    st.info(f"Detected **{explainable_emotion}**, but couldn't extract key contributing words.")

            # Bar Chart
            st.subheader("📈 Confidence Overview")
            df = pd.DataFrame(top_emotions[:3], columns=["Emotion", "Confidence"])
            fig = px.bar(df, x="Emotion", y="Confidence", title="Top 3 Emotions",
                         color="Emotion", text="Confidence", range_y=[0, 1])
            st.plotly_chart(fig, use_container_width=True)

# Weekly Emotional Check-in
if "last_checkin" not in st.session_state or (datetime.now() - st.session_state["last_checkin"]).days >= 7:
    st.subheader("📝 Weekly Reflection")
    user_response = st.text_area("How are you feeling this week?")
    if st.button("Submit Reflection"):
        if user_response.strip():
            add_checkin(st.session_state["user"], user_response)
            st.session_state["last_checkin"] = datetime.now()
            st.success("Your reflection has been saved!")
        else:
            st.warning("Please share your thoughts.")
