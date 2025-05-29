"""
File: database.py
Description: Database configuration for FastAPI application using SQLAlchemy.
Author: Gizachew Kassa
Date Created: 2025-05-28
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Use environment variable or fallback default
db_url = os.getenv("SQLALCHEMY_DATABASE_URL")
if not db_url:
    raise RuntimeError("Environment variable SQLALCHEMY_DATABASE_URL not set")

DATABASE_URL = db_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare Base here to be shared across models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
