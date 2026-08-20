# URL Shortener API

A basic URL shortening REST API built using FastAPI and PostgreSQL.

## Features

- Create shortened URLs
- Generate unique short codes
- Store URL mappings in PostgreSQL
- Redirect short URLs to original URLs
- URL validation
- 404 handling for invalid short codes

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn

## API Endpoints

### POST /shorten

Accepts a long URL and returns a shortened URL.

Request:

{
  "url": "https://www.example.com"
}

Response:

{
  "short_url": "http://localhost:8000/abc123"
}

### GET /{short_code}

Redirects the user to the original URL associated with the short code.

## Database

The application uses PostgreSQL with a `urls` table containing:

- `id`
- `short_code`
- `original_url`
- `created_at`

`short_code` is unique and indexed for efficient lookup.

## How to Run

### 1. Create virtual environment

python -m venv venv

### 2. Activate environment

Windows:

venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure environment

Create a `.env` file:

DB_PASSWORD=your_postgresql_password

### 5. Run the application

uvicorn app.main:app --reload

### 6. Open Swagger UI

http://127.0.0.1:8000/docs

## Current Scope

This implementation focuses on the core URL shortening functionality required by the assessment. Future iterations may introduce caching, horizontal scaling, high availability, and additional security controls.