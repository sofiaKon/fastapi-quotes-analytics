from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.crawler import crawl_top_categories
from app.services import analysis

from app import crud, schemas
from app.database import get_db

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import analysis

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    return analysis.get_summary_stats_api(db)


@router.get("/top-authors")
def get_top_authors(db: Session = Depends(get_db)):
    return analysis.get_top_authors_api(db)


@router.get("/categories")
def get_categories_count(db: Session = Depends(get_db)):
    return analysis.get_categories_count_api(db)


@router.get("/word-count")
def get_word_count(db: Session = Depends(get_db)):
    return analysis.get_word_count_api(db)
