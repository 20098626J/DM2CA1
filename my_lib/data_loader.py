import pandas as pd
import os
from my_lib.pdf_parser import parse_all_pdfs
import streamlit as st

EXAM_FOLDER = "exams"
@st.cache_data(show_spinner="Parsing exam papers...")

def load_data():
    rows = parse_all_pdfs(EXAM_FOLDER)
    if not rows:
        return pd.DataFrame(columns=[
            "filename", "year", "institution", "semester",
            "question_number", "part", "text", "marks", "topic"
        ])
    df = pd.DataFrame(rows)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["marks"] = pd.to_numeric(df["marks"], errors="coerce")
    df["text"] = df["text"].fillna("").str.strip()
    df["topic"] = df["topic"].fillna("General")
    df = df[df["is_marking_scheme"] == False].reset_index(drop=True)
    return df