import streamlit as st
from my_lib import get_topic_summary
from my_lib.filters import get_questions_by_topic


def build(df):
    st.header("Topic Explorer")
    st.markdown("Explore questions grouped by topic across all exam years.")

    if df.empty:
        st.warning("No data available.")
        return

    topic_summary = get_topic_summary(df)
    topics = topic_summary["topic"].tolist()

    selected_topic = st.selectbox("Select a Topic", topics)

    if selected_topic:
        topic_df = get_questions_by_topic(df, selected_topic)

        col1, col2, col3 = st.columns(3)
        col1.metric("Questions", len(topic_df))
        col2.metric("Avg Marks", f"{topic_df['marks'].mean():.1f}" if not topic_df['marks'].isna().all() else "N/A")
        col3.metric("Years Appeared", topic_df["year"].nunique())

        st.divider()

        # Group by year
        for year in sorted(topic_df["year"].dropna().unique(), reverse=True):
            year_df = topic_df[topic_df["year"] == year]
            st.subheader(f"{int(year)}")
            for _, row in year_df.iterrows():
                with st.expander(f"Q{int(row['question_number'])}{row['part']} — {int(row['marks']) if row['marks'] == row['marks'] else '?'} marks"):
                    st.write(row["text"])
