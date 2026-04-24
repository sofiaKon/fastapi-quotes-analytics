from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.crawler import crawl_top_categories
from app.services import analysis

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="",
    tags=["Quotes"]
)


@router.post("/quotes", response_model=schemas.QuoteResponse)
def create_quote(quote: schemas.QuoteCreate, db: Session = Depends(get_db)):
    return crud.create_quote(db=db, quote=quote)


@router.get("/quotes", response_model=List[schemas.QuoteResponse])
def read_all_quotes(db: Session = Depends(get_db)):
    return crud.get_all_quotes(db=db)


@router.get("/quotes/{quote_id}", response_model=schemas.QuoteResponse)
def read_quote_by_id(quote_id: int, db: Session = Depends(get_db)):
    db_quote = crud.get_quote_by_id(db=db, quote_id=quote_id)

    if db_quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")

    return db_quote


@router.put("/quotes/{quote_id}", response_model=schemas.QuoteResponse)
def update_quote(quote_id: int, quote: schemas.QuoteUpdate, db: Session = Depends(get_db)):
    db_quote = crud.update_quote(db=db, quote_id=quote_id, quote=quote)

    if db_quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")

    return db_quote


@router.delete("/quotes/{quote_id}", response_model=schemas.QuoteResponse)
def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    db_quote = crud.delete_quote(db=db, quote_id=quote_id)

    if db_quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")

    return db_quote


@router.post("/crawl")
def crawl_data(db: Session = Depends(get_db)):
    return crawl_top_categories(db)
