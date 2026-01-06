from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Check if we should use local SQLite database
USE_LOCAL_DB = os.getenv("USE_LOCAL_DB", "true").lower() == "true"

if USE_LOCAL_DB:
    # Use SQLite for local development
    DATABASE_URL = "sqlite:///./budget_app.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # Use PostgreSQL for production/Docker
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://budget_user:budget_password@localhost:5432/budget_db")
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()