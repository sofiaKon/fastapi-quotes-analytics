from sqlalchemy.orm import Session
from app import models, schemas


def create_quote(db: Session, quote: schemas.QuoteCreate):
    db_quote = models.Quote(
        text=quote.text,
        author=quote.author,
        category=quote.category
    )
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


def get_all_quotes(db: Session):
    return db.query(models.Quote).all()


def get_quote_by_id(db: Session, quote_id: int):
    return db.query(models.Quote).filter(models.Quote.id == quote_id).first()


def update_quote(db: Session, quote_id: int, quote: schemas.QuoteUpdate):
    db_quote = db.query(models.Quote).filter(
        models.Quote.id == quote_id).first()

    if db_quote is None:
        return None

    db_quote.text = quote.text
    db_quote.author = quote.author
    db_quote.category = quote.category

    db.commit()
    db.refresh(db_quote)
    return db_quote


def delete_quote(db: Session, quote_id: int):
    db_quote = db.query(models.Quote).filter(
        models.Quote.id == quote_id).first()

    if db_quote is None:
        return None

    db.delete(db_quote)
    db.commit()
    return db_quote


def delete_all_quotes(db: Session):
    db.query(models.Quote).delete()
    db.commit()


def quote_exists(db: Session, text: str, category: str):
    return db.query(models.Quote).filter(
        models.Quote.text == text,
        models.Quote.category == category
    ).first() is not None


def count_quotes_by_category(db: Session, category: str):
    return db.query(models.Quote).filter(
        models.Quote.category == category
    ).count()
