import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) #it is responsible for connecting SQLAlchemy to PostgreSQL.

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
#SessionLocal gives us database sessions that we'll use when handling API requests.

Base = declarative_base() #this will be used to define our database tables.

#function that gives each API request a database session and closes it afterward.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()