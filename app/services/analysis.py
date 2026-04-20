from collections import Counter
import pandas as pd
from sqlalchemy.orm import Session
from app import crud


def get_word_count_df(db: Session):
    quotes = crud.get_all_quotes(db)
    words = []

    for q in quotes:
        text = q.text.lower()
        for ch in ['“', '”', '.', ',', '!', '?', ';', ':', '(', ')', '-', '—']:
            text = text.replace(ch, '')
        words.extend(text.split())

    counter = Counter(words)
    top_words = counter.most_common(10)

    return pd.DataFrame(top_words, columns=["Word", "Count"])


def get_top_authors_df(db: Session):
    quotes = crud.get_all_quotes(db)
    authors = [q.author for q in quotes]

    counter = Counter(authors)
    top_authors = counter.most_common(10)

    return pd.DataFrame(top_authors, columns=["Author", "Count"])


def get_categories_count_df(db: Session):
    quotes = crud.get_all_quotes(db)
    categories = [q.category for q in quotes]

    counter = Counter(categories)
    top_categories = counter.most_common()

    return pd.DataFrame(top_categories, columns=["Category", "Count"])


def get_summary_stats(db: Session):
    quotes = crud.get_all_quotes(db)

    total_quotes = len(quotes)
    total_authors = len(set(q.author for q in quotes))
    total_categories = len(set(q.category for q in quotes))

    return total_quotes, total_authors, total_categories
