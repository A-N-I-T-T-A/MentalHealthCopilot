import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import get_entries, delete_entry, get_entries_grouped_by_date
from utils.auth import require_login
require_login()

# Show sidebar
from utils.sidebar import show_sidebar
show_sidebar()




st.title("📖 Your Journal History")

user = st.session_state["user"]

try:
    entries = get_entries(user)

    if not entries:
        st.info("No journal entries found yet. Start writing your first entry!")
    else:
        df = pd.DataFrame(entries, columns=["ID", "User", "Entry", "Emotion", "Confidence", "Timestamp"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        # Sidebar filters
        st.sidebar.header("Filter Entries")
        emotions = ["All"] + sorted(df["Emotion"].unique())
        selected_emotion = st.sidebar.selectbox("Filter by Emotion", emotions)
        min_date = df["Timestamp"].min()
        max_date = df["Timestamp"].max()
        start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date.date(), max_date.date()])

        filtered_df = df.copy()
        if selected_emotion != "All":
            filtered_df = filtered_df[filtered_df["Emotion"] == selected_emotion]
        if start_date and end_date:
            filtered_df = filtered_df[
                (filtered_df["Timestamp"].dt.date >= start_date) &
                (filtered_df["Timestamp"].dt.date <= end_date)
            ]

        if filtered_df.empty:
            st.info("No entries match the selected filters.")
        else:
            st.subheader("Your Entries")
            for idx, row in filtered_df.iterrows():
                with st.expander(f"{row['Timestamp']} - {row['Emotion'].title()}"):
                    st.write(f"**Entry:** {row['Entry']}")
                    st.write(f"**Confidence:** {row['Confidence']:.2f}")
                    if st.button("Delete Entry", key=row["ID"]):
                        delete_entry(row["ID"])
                        st.switch_page("pages/History.py")

        # 📅 Enhanced Mood Calendar Visualization
        st.subheader("📆 Your Mood Calendar")
        
        # Create a comprehensive mood calendar
        if not df.empty:
            # Prepare data for calendar view
            df['Date'] = df['Timestamp'].dt.date
            df['Month'] = df['Timestamp'].dt.to_period('M')
            
            # Create emotion color mapping
            emotion_colors = {
                'happy': '#28a745',      # Green
                'sad': '#6f42c1',        # Purple
                'angry': '#dc3545',      # Red
                'fear': '#fd7e14',       # Orange
                'surprise': '#20c997',   # Teal
                'disgust': '#6c757d',    # Gray
                'neutral': '#17a2b8'     # Blue
            }
            
            # Get unique emotions and assign colors
            unique_emotions = df['Emotion'].unique()
            available_colors = list(emotion_colors.values())[:len(unique_emotions)]
            emotion_color_map = dict(zip(unique_emotions, available_colors))
            
            # Create daily mood summary
            daily_moods = df.groupby('Date')['Emotion'].apply(lambda x: x.mode().iloc[0] if not x.empty else 'neutral').reset_index()
            daily_moods['Color'] = daily_moods['Emotion'].map(emotion_color_map)
            daily_moods['Date'] = pd.to_datetime(daily_moods['Date'])
            
            # Create calendar heatmap
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            # Create a proper calendar layout
            fig = go.Figure()
            
            # Add scatter plot for each day with mood
            for emotion in unique_emotions:
                emotion_data = daily_moods[daily_moods['Emotion'] == emotion]
                if not emotion_data.empty:
                    fig.add_trace(go.Scatter(
                        x=emotion_data['Date'],
                        y=[1] * len(emotion_data),  # Fixed y position for calendar view
                        mode='markers',
                        marker=dict(
                            size=20,
                            color=emotion_color_map[emotion],
                            symbol='circle',
                            line=dict(width=2, color='white')
                        ),
                        name=emotion.title(),
                        hovertemplate=f'<b>{emotion.title()}</b><br>Date: %{{x}}<extra></extra>'
                    ))
            
            # Update layout for better calendar appearance
            fig.update_layout(
                title="📅 Your Mood Calendar - Daily Mood Tracking",
                xaxis_title="Date",
                yaxis=dict(showticklabels=False, range=[0.5, 1.5]),
                height=400,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add mood trend over time
            st.subheader("📈 Mood Trend Over Time")
            
            # Create weekly mood summary
            df['Week'] = df['Timestamp'].dt.to_period('W')
            weekly_moods = df.groupby('Week')['Emotion'].apply(lambda x: x.mode().iloc[0] if not x.empty else 'neutral').reset_index()
            weekly_moods['Week_Start'] = weekly_moods['Week'].dt.start_time
            
            # Create trend line
            fig_trend = px.line(
                weekly_moods, 
                x='Week_Start', 
                y='Emotion',
                title="Weekly Mood Trend",
                color_discrete_sequence=['#667eea']
            )
            fig_trend.update_layout(
                height=300,
                xaxis_title="Week",
                yaxis_title="Dominant Mood"
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Add emotion distribution pie chart
            st.subheader("🎭 Overall Mood Distribution")
            emotion_counts = df['Emotion'].value_counts()
            
            fig_pie = px.pie(
                values=emotion_counts.values,
                names=emotion_counts.index,
                title="Your Mood Distribution",
                color_discrete_sequence=list(emotion_color_map.values())
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Add mood insights
            st.subheader("💡 Mood Insights")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                most_common = df['Emotion'].mode().iloc[0]
                st.metric("Most Common Mood", most_common.title(), help="Your most frequent emotion")
            
            with col2:
                total_entries = len(df)
                st.metric("Total Entries", total_entries, help="Total journal entries")
            
            with col3:
                days_active = df['Date'].nunique()
                st.metric("Days Active", days_active, help="Days you've journaled")
            
        
        else:
            st.info("No data available for calendar visualization.")

except Exception as e:
    st.error(f"An error occurred while loading entries: {e}")
