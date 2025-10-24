# pages/Trends.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import get_entries
from utils.auth import require_login
require_login()

# Show sidebar
from utils.sidebar import show_sidebar
show_sidebar()

st.title("📈 Emotion Trends Over Time")
user = st.session_state["user"]

try:
    entries = get_entries(user)

    if not entries:
        st.info("No journal entries found yet. Start writing your first entry!")
    else:
        # Convert to DataFrame
        df = pd.DataFrame(entries, columns=["ID", "User", "Entry", "Emotion", "Confidence", "Timestamp"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        # Sidebar filters
        st.sidebar.header("Filter Entries")

        # Date range filter
        min_date = df["Timestamp"].min().date()
        max_date = df["Timestamp"].max().date()
        start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

        # Apply date filter
        filtered_df = df[
            (df["Timestamp"].dt.date >= start_date) &
            (df["Timestamp"].dt.date <= end_date)
        ]

        if filtered_df.empty:
            st.info("No entries found for the selected date range.")
        else:
            # Aggregate by date and emotion
            emotion_counts = filtered_df.groupby([filtered_df["Timestamp"].dt.date, "Emotion"]).size().reset_index(name="Count")

            # Stacked Bar Chart
            fig = px.bar(emotion_counts, x="Timestamp", y="Count", color="Emotion", title="Emotion Trends Over Time (Stacked)",
                         labels={"Timestamp": "Date", "Count": "Number of Entries"}, height=600)

            fig.update_layout(barmode='stack', xaxis_title='Date', yaxis_title='Count')

            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred while loading entries: {e}")
