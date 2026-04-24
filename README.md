# Quotes Analytics System

A full-stack web project that collects quotes from a public website, stores them in a database, provides REST API endpoints, and offers an analytics dashboard through Gradio.

## Project Overview

This project was built to practice a real-world backend and data workflow in one system:

- web crawling
- database storage
- RESTful API development
- data analysis
- UI integration
- Docker deployment

The application collects quotes from **quotes.toscrape.com**, stores them in **SQLite**, manages them with **FastAPI**, and visualizes analytics with **Gradio**.

---

## Main Features

### 1. Web Crawling

- Crawls quotes from `quotes.toscrape.com`
- Extracts quote text, author, and category
- Selects categories based on website tags
- Tries to collect up to 20 quotes per category
- Saves crawled data into the database

### 2. Database Storage

The project uses **SQLite** with SQLAlchemy ORM.

Main table: `quotes`

Fields:

- `id`
- `text`
- `author`
- `category`

### 3. REST API with FastAPI

The backend provides CRUD endpoints for quote management.

#### Quotes API

- `POST /quotes` → create a quote
- `GET /quotes` → get all quotes
- `GET /quotes/{quote_id}` → get one quote
- `PUT /quotes/{quote_id}` → update a quote
- `DELETE /quotes/{quote_id}` → delete a quote

#### Crawler API

- `POST /crawl` → crawl and store quotes automatically

#### Analytics API

- `GET /analytics/summary` → get total quotes, authors, and categories
- `GET /analytics/top-authors` → get top authors
- `GET /analytics/categories` → get category counts
- `GET /analytics/word-count` → get most common words

### 4. Gradio UI

Gradio is mounted inside the FastAPI application.

Available at:

```bash
/ui

```
UI includes:

- dashboard metrics
- quotes table
- crawl button
- word frequency analysis
- top authors analysis
- category distribution analysis
- project report tab

### 5. Basic Data Analysis

The project provides:

- Word Count
- Top Authors
- Category Count
- bar chart visualization with Matplotlib

---

Tech Stack

- FastAPI — backend API
- SQLAlchemy — database ORM
- SQLite — local database
- BeautifulSoup4 — web crawling
- Requests — HTTP requests
- Gradio — UI
- Pandas — tabular data handling
- Matplotlib — charts
- Docker — deployment packaging
- Railway — cloud deployment

---

Project Structure

```bash
fastapi-quotes-analytics/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │             ├── analys.py
│   │             └── quotes.py
│   ├── services/
│   │   ├── crawler.py
│   │   └── analysis.py
│   ├── ui/
│   │   └── gradio_app.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── data/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── run.py
└── README.md

```
---

### How the System Works

Data Pipeline
1. Crawl quotes from the website
2. Extract text, author, and category
3. Store data in SQLite
4. Serve data through FastAPI endpoints
5. Visualize and analyze data in Gradio

---

### API Endpoints
- Root
| Method | Endpoint | Description   |
| ------ | -------- | ------------- |
| GET    | `/`      | Root endpoint |

- Quotes

| Method | Endpoint             | Description        |
| ------ | -------------------- | ------------------ |
| POST   | `/quotes`            | Create a new quote |
| GET    | `/quotes`            | Get all quotes     |
| GET    | `/quotes/{quote_id}` | Get quote by ID    |
| PUT    | `/quotes/{quote_id}` | Update a quote     |
| DELETE | `/quotes/{quote_id}` | Delete a quote     |

- Analytics

| Method | Endpoint                 | Description            |
| ------ | ------------------------ | ---------------------- |
| GET    | `/analytics/summary`     | Get summary statistics |
| GET    | `/analytics/top-authors` | Get top authors        |
| GET    | `/analytics/categories`  | Get category counts    |
| GET    | `/analytics/word-count`  | Get word frequency     |

---

### Local Installation

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-quotes-analytics.git
cd fastapi-quotes-analytics
```

2. Install dependencies

```bash
pip install -r requirements.txt
```
3. Run the project

```bash
python run.py
```
---

### Local URLs

1. FastAPI

```bash
http://127.0.0.1:8000
```

2. Swagger Docs

```bash
http://127.0.0.1:8000/docs
```

3. Gradio UI

```bash
http://127.0.0.1:8000/ui
```
---

### Deployment

This project was deployed on Railway using Docker.

Deployment setup includes:

- Docker-based build
- public domain through Railway
- SQLite persistence with mounted volume
