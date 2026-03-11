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

print(f"Total question parts: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nMissing values:\n{df.isna().sum()}")
missing_year = df[df['year'].isna()]
print(missing_year['filename'].value_counts())