import streamlit as st
from my_lib import load_data
from pages import home, question_browser, topic_explorer, search


st.set_page_config(
    page_title="DM Exam Viewer",
    page_icon="📚",
    layout="wide"
)

df = load_data()

st.sidebar.title("DM Exam Viewer")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Question Browser", "Topic Explorer", "Keyword Search"]
)

st.sidebar.markdown("---")
st.sidebar.caption(f" {df['filename'].nunique() if not df.empty else 0} exam papers loaded")
st.sidebar.caption(f" {len(df)} question parts indexed")

if page == "Home":
    home.build(df)
elif page == "Question Browser":
    question_browser.build(df)
elif page == "Topic Explorer":
    topic_explorer.build(df)
elif page == "Keyword Search":
    search.build(df)

