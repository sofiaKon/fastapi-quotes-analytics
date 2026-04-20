FROM python:3.11-slim

WORKDIR /app

# system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# install dependencies first for better layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# make sure data directory exists
RUN mkdir -p /app/data

# Railway provides PORT automatically
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"