import secrets
import string

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import URL
from .schemas import URLCreate, URLResponse


# to create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortening API built with FastAPI and PostgreSQL.",
    version="1.0.0",
)


def generate_short_code(length: int = 6) -> str:
    """Generate a random alphanumeric short code."""
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


@app.get("/")
def root():
    return {"message": "URL Shortener API is running"}


@app.post("/shorten", response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    """Create a shortened URL and store it in PostgreSQL."""

    # to generate a unique short code
    while True:
        short_code = generate_short_code()

        existing_url = (
            db.query(URL)
            .filter(URL.short_code == short_code)
            .first()
        )

        if not existing_url:
            break

    # for storing the URL
    new_url = URL(
        short_code=short_code,
        original_url=str(url_data.url),
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return URLResponse(
        short_url=f"http://localhost:8000/{short_code}"
    )


@app.get("/{short_code}")
def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db),
):
    """Redirect a short URL to its original URL."""

    url_record = (
        db.query(URL)
        .filter(URL.short_code == short_code)
        .first()
    )

    if not url_record:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    return RedirectResponse(
        url=url_record.original_url,
        status_code=307,
    )