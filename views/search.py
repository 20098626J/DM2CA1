import streamlit as st
from my_lib import keyword_search


def build(df):
    st.header("Keyword Search")
    st.markdown("Search for any word or phrase across all exam questions.")

    if df.empty:
        st.warning("No data available.")
        return

    keyword = st.text_input("Enter keyword or phrase", placeholder="e.g. Venn diagram, truth table, Eulerian...")

    if not keyword:
        st.info("Type a keyword above to search.")
        return

    results = keyword_search(df, keyword)

    if results.empty:
        st.warning(f"No questions found containing **'{keyword}'**.")
        return

    st.success(f"Found **{len(results)}** question(s) containing **'{keyword}'**")
    st.divider()

    for _, row in results.iterrows():
        marks_display = int(row['marks']) if row['marks'] == row['marks'] else '?'
        with st.expander(
            f"{int(row['year'])} | Q{int(row['question_number'])}{row['part']} | "
            f"{row['topic']} | {marks_display} marks"
        ):
            st.markdown(f"**Topic:** {row['topic']} &nbsp;&nbsp; **Year:** {int(row['year'])} &nbsp;&nbsp; **Marks:** {marks_display}")
            st.divider()

            #Highlight keyword in text
            text = row["text"]
            highlighted = text.replace(
                keyword, f"**:orange[{keyword}]**"
            ).replace(
                keyword.lower(), f"**:orange[{keyword.lower()}]**"
            ).replace(
                keyword.capitalize(), f"**:orange[{keyword.capitalize()}]**"
            )
            st.markdown(highlighted)
