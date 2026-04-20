import gradio as gr
import pandas as pd
from sqlalchemy.orm import Session
import matplotlib.pyplot as plt

from app.database import SessionLocal
from app import crud
from app.services.analysis import (
    get_word_count_df,
    get_top_authors_df,
    get_categories_count_df,
    get_summary_stats
)
from app.services.crawler import crawl_top_categories


def fetch_quotes_table():
    db: Session = SessionLocal()
    try:
        quotes = crud.get_all_quotes(db)

        data = [
            {
                "ID": q.id,
                "Quote": q.text,
                "Author": q.author,
                "Category": q.category
            }
            for q in quotes
        ]

        return pd.DataFrame(data)
    finally:
        db.close()


def run_crawl_and_refresh():
    db: Session = SessionLocal()
    try:
        result = crawl_top_categories(db, top_n=5, quotes_per_category=20)
        total_quotes, total_authors, total_categories = get_summary_stats(db)
        quotes_df = fetch_quotes_table()

        status_text = (
            f"Selected categories: {', '.join(result['selected_categories'])}\n"
            f"Total saved: {result['total_saved']}\n"
            f"Per category: {result['quotes_per_category']}"
        )

        return (
            status_text,
            total_quotes,
            total_authors,
            total_categories,
            quotes_df
        )
    finally:
        db.close()


def load_dashboard_stats():
    db: Session = SessionLocal()
    try:
        total_quotes, total_authors, total_categories = get_summary_stats(db)
        return total_quotes, total_authors, total_categories
    finally:
        db.close()


def create_bar_chart(df, label_col, title):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df[label_col], df["Count"])
    ax.set_title(title)
    ax.set_xlabel(label_col)
    ax.set_ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig


def load_word_analysis():
    db: Session = SessionLocal()
    try:
        df = get_word_count_df(db)
        fig = create_bar_chart(df, "Word", "Top Words")
        return df, fig
    finally:
        db.close()


def load_author_analysis():
    db: Session = SessionLocal()
    try:
        df = get_top_authors_df(db)
        fig = create_bar_chart(df, "Author", "Top Authors")
        return df, fig
    finally:
        db.close()


def load_category_analysis():
    db: Session = SessionLocal()
    try:
        df = get_categories_count_df(db)
        fig = create_bar_chart(df, "Category", "Category Distribution")
        return df, fig
    finally:
        db.close()


def create_interface():
    with gr.Blocks(title="Quotes Analytics System") as demo:
        gr.Markdown(
            """
            # Quotes Analytics System
            FastAPI + SQLite + Gradio 기반 격언 관리 및 분석 시스템  
            크롤링, CRUD API, 데이터 분석 기능을 하나의 서비스로 통합했습니다.
            """
        )

        with gr.Row():
            total_quotes_box = gr.Number(
                label="Total Quotes", interactive=False)
            total_authors_box = gr.Number(
                label="Total Authors", interactive=False)
            total_categories_box = gr.Number(
                label="Total Categories", interactive=False)

        with gr.Row():
            load_stats_btn = gr.Button("Load Dashboard")
            crawl_btn = gr.Button("Crawl New Quotes")

        crawl_status = gr.Textbox(label="Crawl Status", interactive=False)

        with gr.Tabs():
            with gr.Tab("Quotes"):
                gr.Markdown("### Quotes Table")
                load_quotes_btn = gr.Button("Show Quotes")
                quotes_table = gr.Dataframe(
                    headers=["ID", "Quote", "Author", "Category"],
                    label="Stored Quotes",
                    interactive=False
                )

            with gr.Tab("Analysis"):
                gr.Markdown("### Basic Text Analysis")

                with gr.Row():
                    word_btn = gr.Button("Word Count")
                    author_btn = gr.Button("Top Authors")
                    category_btn = gr.Button("Category Count")

                analysis_table = gr.Dataframe(
                    label="Analysis Result",
                    interactive=False,
                    wrap=True
                )

                analysis_chart = gr.Plot(label="Analysis Chart")
            with gr.Tab("Report"):
                gr.Markdown("""
                ##  Project Overview

                ###  Project Goal
                This project builds a full-stack system for collecting, storing, and analyzing quotes using modern web development tools.

                ###  Tech Stack
                - FastAPI (Backend API)
                - SQLite (Database)
                - BeautifulSoup (Web Crawling)
                - Gradio (UI)

                ###  Data Pipeline
                1. Crawl quotes from website
                2. Store in SQLite database
                3. Provide REST API (CRUD)
                4. Visualize data via Gradio UI

                ###  Category Selection Logic
                - Extract all tags from website
                - Select top 5 categories
                - Collect up to 20 unique quotes per category
                - Avoid duplicates within same category

                ###  Result
                - 5 categories
                - Up to 100 quotes total
                - Basic text analysis (word frequency, authors, categories)

                ###  Features
                - CRUD API
                - Crawling system
                - Dashboard metrics
                - Text analytics

                ---
                Made with FastAPI + Gradio 
                """)

        load_stats_btn.click(
            fn=load_dashboard_stats,
            inputs=[],
            outputs=[total_quotes_box, total_authors_box, total_categories_box]
        )

        load_quotes_btn.click(
            fn=fetch_quotes_table,
            inputs=[],
            outputs=quotes_table
        )

        crawl_btn.click(
            fn=run_crawl_and_refresh,
            inputs=[],
            outputs=[
                crawl_status,
                total_quotes_box,
                total_authors_box,
                total_categories_box,
                quotes_table
            ]
        )

        word_btn.click(
            fn=load_word_analysis,
            inputs=[],
            outputs=[analysis_table, analysis_chart]
        )

        author_btn.click(
            fn=load_author_analysis,
            inputs=[],
            outputs=[analysis_table, analysis_chart]
        )

        category_btn.click(
            fn=load_category_analysis,
            inputs=[],
            outputs=[analysis_table, analysis_chart]
        )

    return demo
