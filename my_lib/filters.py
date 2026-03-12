import pandas as pd

def apply_filters(df, years=None, topics=None, min_marks=None, max_marks=None, question_numbers=None):
    
    filtered = df.copy()

    if years:
        filtered = filtered[filtered["year"].isin(years)]

    if topics:
        filtered = filtered[filtered["topic"].isin(topics)]

    if min_marks is not None:
        filtered = filtered[filtered["marks"] >= min_marks]

    if max_marks is not None:
        filtered = filtered[filtered["marks"] <= max_marks]

    if question_numbers:
        filtered = filtered[filtered["question_number"].isin(question_numbers)]

    return filtered.reset_index(drop=True)


def keyword_search(df, keyword):
    
    if not keyword or not keyword.strip():
        return df

    kw = keyword.strip().lower()
    mask = df["text"].str.lower().str.contains(kw, na=False)
    result = df[mask].copy()

    result["match_score"] = result["text"].str.lower().str.count(kw)
    result = result.sort_values("match_score", ascending=False)

    return result.reset_index(drop=True)


def get_questions_by_topic(df, topic):
    
    return df[df["topic"] == topic].reset_index(drop=True)


def get_questions_by_year(df, year):
    
    return df[df["year"] == year].reset_index(drop=True)


def get_topic_summary(df):
    
    summary = df.groupby("topic").agg(
        question_count=("text", "count"),
        avg_marks=("marks", "mean"),
        years_appeared=("year", lambda x: sorted(x.dropna().astype(int).unique().tolist()))
    ).reset_index()
    summary["avg_marks"] = summary["avg_marks"].round(1)
    return summary.sort_values("question_count", ascending=False)


def get_year_summary(df):
    
    summary = df.groupby("year").agg(
        question_count=("text", "count"),
        topics_covered=("topic", lambda x: len(x.unique())),
        total_marks=("marks", "sum")
    ).reset_index()
    summary["year"] = summary["year"].astype(int)
    return summary.sort_values("year", ascending=True)
