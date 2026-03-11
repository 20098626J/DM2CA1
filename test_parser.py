from my_lib.pdf_parser import parse_all_pdfs
import pandas as pd

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