import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from my_lib import get_year_summary, get_topic_summary


def build(df):
    st.title("Discrete Mathematics Exam Viewer")
    st.markdown("Browse, search and filter past exam questions.")

    if df.empty:
        st.warning("No exam papers found.")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Exam Papers", df["filename"].nunique())
    col2.metric("Total Questions", len(df))
    col3.metric("Topics", df["topic"].nunique())
    col4.metric("Years Covered", f"{int(df['year'].min())} – {int(df['year'].max())}")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Questions per Year")
        year_summary = get_year_summary(df)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(year_summary["year"].astype(str), year_summary["question_count"], color="#4C72B0")
        ax.set_xlabel("Year")
        ax.set_ylabel("Questions")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    with col_right:
        st.subheader("Questions by Topic")
        topic_summary = get_topic_summary(df)
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        ax2.pie(
            topic_summary["question_count"],
            labels=topic_summary["topic"],
            autopct="%1.0f%%",
            startangle=140
        )
        plt.tight_layout()
        st.pyplot(fig2)

    st.divider()

    st.subheader("Topic Overview")
    display = topic_summary.rename(columns={
        "topic": "Topic",
        "question_count": "# Questions",
        "avg_marks": "Avg Marks",
        "years_appeared": "Years Appeared"
    })
    st.dataframe(display, use_container_width=True, hide_index=True)
