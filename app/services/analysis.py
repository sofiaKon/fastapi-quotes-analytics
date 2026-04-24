from collections import Counter
import pandas as pd
from sqlalchemy.orm import Session
from app import crud


def clean_text(text: str) -> str:
    """
    Cleans quote text for word counting.
    """
    text = text.lower()

    for ch in ['“', '”', '"', "'", '.', ',', '!', '?', ';', ':', '(', ')', '-', '—']:
        text = text.replace(ch, '')

    return text


# =========================
# DataFrame functions
# For Gradio / charts
# =========================

def get_word_count_df(db: Session) -> pd.DataFrame:
    quotes = crud.get_all_quotes(db)
    words = []

    for quote in quotes:
        text = clean_text(quote.text)
        words.extend(text.split())

    counter = Counter(words)
    top_words = counter.most_common(10)

    return pd.DataFrame(top_words, columns=["Word", "Count"])


def get_top_authors_df(db: Session) -> pd.DataFrame:
    quotes = crud.get_all_quotes(db)
    authors = [quote.author for quote in quotes]

    counter = Counter(authors)
    top_authors = counter.most_common(10)

    return pd.DataFrame(top_authors, columns=["Author", "Count"])


def get_categories_count_df(db: Session) -> pd.DataFrame:
    quotes = crud.get_all_quotes(db)
    categories = [quote.category for quote in quotes]

    counter = Counter(categories)
    categories_count = counter.most_common()

    return pd.DataFrame(categories_count, columns=["Category", "Count"])


# =========================
# Summary
# =========================

def get_summary_stats(db: Session) -> tuple[int, int, int]:
    quotes = crud.get_all_quotes(db)

    total_quotes = len(quotes)
    total_authors = len(set(quote.author for quote in quotes))
    total_categories = len(set(quote.category for quote in quotes))

    return total_quotes, total_authors, total_categories


# =========================
# API functions
# For FastAPI JSON response
# =========================

def get_summary_stats_api(db: Session) -> dict:
    total_quotes, total_authors, total_categories = get_summary_stats(db)

    return {
        "total_quotes": total_quotes,
        "total_authors": total_authors,
        "total_categories": total_categories
    }


def get_word_count_api(db: Session) -> list[dict]:
    df = get_word_count_df(db)
    return df.to_dict(orient="records")


def get_top_authors_api(db: Session) -> list[dict]:
    df = get_top_authors_df(db)
    return df.to_dict(orient="records")


def get_categories_count_api(db: Session) -> list[dict]:
    df = get_categories_count_df(db)
    return df.to_dict(orient="records")
