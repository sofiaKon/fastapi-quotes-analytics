import requests
from bs4 import BeautifulSoup
from collections import Counter
from sqlalchemy.orm import Session

from app import models
from app.crud import delete_all_quotes, quote_exists, count_quotes_by_category


def discover_top_categories(pages: int = 10, top_n: int = 5):
    base_url = "http://quotes.toscrape.com/page/{}/"
    tag_counter = Counter()

    for page in range(1, pages + 1):
        url = base_url.format(page)
        response = requests.get(url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            break

        for q in quotes:
            tags = q.find_all("a", class_="tag")
            for tag in tags:
                tag_name = tag.get_text(strip=True)
                tag_counter[tag_name] += 1

    return [tag for tag, _ in tag_counter.most_common(top_n)]


def crawl_quotes_for_category(db: Session, category: str, limit: int = 20):
    page = 1

    while count_quotes_by_category(db, category) < limit:
        url = f"http://quotes.toscrape.com/tag/{category}/page/{page}/"
        response = requests.get(url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            break

        for q in quotes:
            if count_quotes_by_category(db, category) >= limit:
                break

            text = q.find("span", class_="text").get_text(strip=True)
            author = q.find("small", class_="author").get_text(strip=True)

            if quote_exists(db, text, category):
                continue

            db_quote = models.Quote(
                text=text,
                author=author,
                category=category
            )

            db.add(db_quote)
            db.commit()

        page += 1

    return count_quotes_by_category(db, category)


def crawl_top_categories(db: Session, top_n: int = 5, quotes_per_category: int = 20):
    delete_all_quotes(db)

    top_categories = discover_top_categories(top_n=top_n)

    result = {}

    for category in top_categories:
        saved_count = crawl_quotes_for_category(
            db=db,
            category=category,
            limit=quotes_per_category
        )
        result[category] = saved_count

    total_saved = db.query(models.Quote).count()

    return {
        "selected_categories": top_categories,
        "quotes_per_category": result,
        "total_saved": total_saved
    }
