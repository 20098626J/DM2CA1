from my_lib.pdf_parser import parse_all_pdfs
import pandas as pd
'''
df = pd.DataFrame(parse_all_pdfs("exams"))

print(f"Total question parts found: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nTopics found: {df['topic'].value_counts()}")
general = df[df['topic'] == 'General']
print(general['text'].head(20).to_string())
print(f"\nRows with no marks detected: {df['marks'].isna().sum()}")
print(f"Rows with marks: {df['marks'].notna().sum()}")
'''

from my_lib.data_loader import load_data

df = load_data()
'''
print(f"Total question parts: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values:\n{df.isna().sum()}")
missing_year = df[df['year'].isna()]
print(missing_year['filename'].value_counts())
'''

from my_lib.filters import apply_filters, keyword_search, get_topic_summary, get_year_summary

sets_questions = apply_filters(df, topics=["Sets & Relations"])
print(f"Sets & Relations questions: {len(sets_questions)}")

questions_2013 = apply_filters(df, years=[2013])
print(f"2013 questions: {len(questions_2013)}")

results = keyword_search(df, "venn")
print(f"Questions mentioning 'venn': {len(results)}")

results = keyword_search(df, "Represent the sets")
print(f"Results: {len(results)}")

print(get_topic_summary(df))
print(get_year_summary(df))

sets_df = apply_filters(df, topics=["Sets & Relations"])
for text in sets_df["text"].head(5):
    print(text[:200])
    print("---")

results = keyword_search(df, "digraph")
print(f"Questions mentioning 'digraph': {len(results)}")

results = keyword_search(df, "ordered pairs")
print(f"Questions mentioning 'ordered pairs': {len(results)}")

print(df["marks"].max())
print(df["marks"].value_counts().sort_index())

import fitz
import os

pdf_path = None
for root, _, files in os.walk("exams"):
    for f in files:
        if "2013" in f and "MS" not in f:
            pdf_path = os.path.join(root, f)

if pdf_path:
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        if "15 marks" in text.lower():
            print(text)
            print("---")
    doc.close()