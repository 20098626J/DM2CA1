import streamlit as st
from my_lib import apply_filters, get_filter_options


def build(df):
    st.header("Question Browser")
    st.markdown("Filter questions by year, topic, question number or marks.")

    if df.empty:
        st.warning("No data available.")
        return

    options = get_filter_options(df)

    
    with st.sidebar:
        st.header("Filters")

        selected_years = st.multiselect(
            "Year", options["years"], default=[]
        )
        selected_topics = st.multiselect(
            "Topic", options["topics"], default=[]
        )
        selected_questions = st.multiselect(
            "Question Number", options["questions"], default=[]
        )

        marks_range = st.slider(
            "Marks Range",
            min_value=0,
            max_value=int(df["marks"].max()) if not df["marks"].isna().all() else 20,
            value=(0, int(df["marks"].max()) if not df["marks"].isna().all() else 20)
        )

    
    filtered = apply_filters(
        df,
        years=selected_years if selected_years else None,
        topics=selected_topics if selected_topics else None,
        min_marks=marks_range[0] if marks_range[0] > 0 else None,
        max_marks=marks_range[1],
        question_numbers=selected_questions if selected_questions else None,
    )

    st.markdown(f"**{len(filtered)} question(s) found**")
    st.divider()

    
    if filtered.empty:
        st.info("No questions match your filters.")
        return

    for _, row in filtered.iterrows():
        with st.expander(
            f"{int(row['year'])} | Q{int(row['question_number'])}{row['part']} | "
            f"{row['topic']} | {int(row['marks']) if not __import__('math').isnan(row['marks']) else '?'} marks"
        ):
            st.markdown(f"**Topic:** {row['topic']}")
            st.markdown(f"**Year:** {int(row['year'])} &nbsp;&nbsp; **Part:** {row['part']} &nbsp;&nbsp; **Marks:** {row['marks']}")
            st.markdown("---")
            st.write(row["text"])
