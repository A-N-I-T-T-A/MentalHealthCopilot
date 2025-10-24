# pages/WellnessTools.py
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
from datetime import datetime, timedelta
from utils.db import get_entries
from utils.auth import require_login
require_login()

# Show sidebar
from utils.sidebar import show_sidebar
show_sidebar()

st.title("🌿 Wellness Tools")

user = st.session_state["user"]

# Create tabs
tab1, tab2, tab3 = st.tabs(["🧘 Breathing Exercises", "📊 Mood Summary & Reflection", "📚 Resources & Activities"])

# Tab 1: Breathing Exercises
with tab1:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">🧘 Guided Breathing Exercise</h2>
        <p style="color: #f0f0f0; margin: 10px 0 0 0;">Find your calm with this 4-4-6 breathing technique</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🌟 Start Your Journey to Calm", type="primary", use_container_width=True):
            # Create containers for different elements
            progress_container = st.empty()
            breathing_container = st.empty()
            instruction_container = st.empty()
            cycle_container = st.empty()
            
            # Breathing cycle: Inhale (4s) → Hold (4s) → Exhale (6s)
            for cycle in range(3):
                cycle_container.markdown(f"""
                <div style="text-align: center; padding: 10px; background: #f8f9fa; 
                            border-radius: 10px; margin: 10px 0;">
                    <h3 style="color: #495057; margin: 0;">Cycle {cycle + 1} of 3</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar
                progress_bar = progress_container.progress(0)
                
                # Inhale Phase
                instruction_container.markdown("""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            border-radius: 15px; margin: 10px 0;">
                    <h1 style="color: white; font-size: 3em; margin: 0;">🌬️</h1>
                    <h2 style="color: white; margin: 10px 0;">INHALE</h2>
                    <p style="color: #f0f0f0; margin: 0;">Breathe in slowly and deeply</p>
                </div>
                """, unsafe_allow_html=True)
                
                for i in range(40):  # 4 seconds with 0.1s intervals
                    progress_bar.progress((i + 1) / 40)
                    time.sleep(0.1)
                
                # Hold Phase
                instruction_container.markdown("""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                            border-radius: 15px; margin: 10px 0;">
                    <h1 style="color: white; font-size: 3em; margin: 0;">⏸️</h1>
                    <h2 style="color: white; margin: 10px 0;">HOLD</h2>
                    <p style="color: #f0f0f0; margin: 0;">Keep the breath gently</p>
                </div>
                """, unsafe_allow_html=True)
                
                for i in range(40):  # 4 seconds with 0.1s intervals
                    progress_bar.progress((i + 1) / 40)
                    time.sleep(0.1)
                
                # Exhale Phase
                instruction_container.markdown("""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                            border-radius: 15px; margin: 10px 0;">
                    <h1 style="color: #333; font-size: 3em; margin: 0;">🌪️</h1>
                    <h2 style="color: #333; margin: 10px 0;">EXHALE</h2>
                    <p style="color: #555; margin: 0;">Release slowly and completely</p>
                </div>
                """, unsafe_allow_html=True)
                
                for i in range(60):  # 6 seconds with 0.1s intervals
                    progress_bar.progress((i + 1) / 60)
                    time.sleep(0.1)
                
                if cycle < 2:  # Don't show "Cycle complete" for the last cycle
                    instruction_container.markdown("""
                    <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%); 
                                border-radius: 15px; margin: 10px 0;">
                        <h3 style="color: #333; margin: 0;">✅ Cycle Complete!</h3>
                        <p style="color: #555; margin: 5px 0 0 0;">Taking a gentle pause...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(2)
            
            # Completion message
            instruction_container.markdown("""
            <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 20px; margin: 20px 0;">
                <h1 style="color: white; font-size: 4em; margin: 0;">🎉</h1>
                <h2 style="color: white; margin: 15px 0;">Amazing Work!</h2>
                <p style="color: #f0f0f0; margin: 0; font-size: 1.2em;">You've completed your breathing exercise</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✨ Take a moment to notice how calm and centered you feel now.")
            
            # Clear containers
            progress_container.empty()
            cycle_container.empty()

# Tab 2: Mood Summary & Reflection
with tab2:
    st.subheader("Your Weekly Mood Summary")
    
    # Get user entries
    entries = get_entries(user)
    
    if entries:
        # Convert to DataFrame
        df = pd.DataFrame(entries, columns=['id', 'user', 'entry', 'emotion', 'confidence', 'timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Get entries from the last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        recent_entries = df[df['timestamp'] >= week_ago]
        
        if not recent_entries.empty:
            # Group by emotion and count
            emotion_counts = recent_entries['emotion'].value_counts()
            total_entries = len(recent_entries)
            
            # Create summary text
            emotion_summary = []
            for emotion, count in emotion_counts.items():
                emotion_summary.append(f"{emotion} ({count})")
            
            summary_text = f"This week, you logged {total_entries} entries: {', '.join(emotion_summary)}."
            st.info(summary_text)
            
            # Show emotion distribution chart
            if len(emotion_counts) > 1:
                fig = px.pie(values=emotion_counts.values, names=emotion_counts.index, 
                           title="Weekly Emotion Distribution")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No entries found for this week. Start journaling to see your mood patterns!")
    else:
        st.info("No journal entries found. Start journaling to see your mood patterns!")
    
    # Reflection prompts
    st.subheader("💭 Reflection Prompts")
    reflection_prompts = [
        "What patterns do you notice in your emotions this week?",
        "What activities or moments brought you the most joy recently?",
        "How have you been taking care of yourself lately?",
        "What would you like to focus on for your mental wellness this week?",
        "What's one thing you're grateful for today?"
    ]
    
    selected_prompt = random.choice(reflection_prompts)
    st.write(f"**Today's reflection question:** {selected_prompt}")
    
    reflection_response = st.text_area("Your reflection:", height=100)
    if st.button("Save Reflection"):
        if reflection_response.strip():
            st.success("Your reflection has been saved! 💝")
        else:
            st.warning("Please share your thoughts.")

# Tab 3: Resources & Activities
with tab3:
    st.subheader("Self-Care Activities")
    
    # Activities organized by category
    activities = {
        "anxiety": [
            "Practice the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
            "Try progressive muscle relaxation - tense and release each muscle group",
            "Write down your worries and then challenge each one with evidence",
            "Take a warm bath or shower to relax your body"
        ],
        "sadness": [
            "Listen to uplifting music or a favorite playlist",
            "Reach out to a friend or family member for support",
            "Engage in gentle physical activity like walking or stretching",
            "Write a gratitude list of 3 things you appreciate",
            "Watch a funny movie or comedy show"
        ],
        "general": [
            "Spend 10 minutes in nature or near a window with natural light",
            "Practice mindful eating - savor each bite slowly",
            "Do a digital detox for 30 minutes",
            "Try a new hobby or creative activity",
            "Get adequate sleep (7-9 hours)",
            "Stay hydrated and eat nourishing foods"
        ]
    }
    
    # Display random activities
    st.write("**Here are some activities to try today:**")
    
    # Select random activities from different categories
    selected_activities = []
    for category, activity_list in activities.items():
        selected_activities.extend(random.sample(activity_list, min(1, len(activity_list))))
    
    # Show 2-3 random activities
    display_activities = random.sample(selected_activities, min(3, len(selected_activities)))
    
    for i, activity in enumerate(display_activities, 1):
        st.write(f"{i}. {activity}")
    
    if st.button("Get New Activities"):
        st.rerun()
    
    # Trusted Resources section
    st.subheader("🌐 Trusted Resources")
    st.write("**Professional Mental Health Resources:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**World Health Organization (WHO)**")
        st.markdown("[Mental Health Resources](https://www.who.int/mental_health)")
        st.markdown("Global mental health information and resources")
    
    with col2:
        st.markdown("**National Institute of Mental Health (NIMH)**")
        st.markdown("[NIMH Resources](https://www.nimh.nih.gov)")
        st.markdown("Research-based mental health information")
    
    st.markdown("---")
    st.info("💡 **Remember:** These tools are for general wellness. If you're experiencing a mental health crisis, please contact a mental health professional or emergency services.")
