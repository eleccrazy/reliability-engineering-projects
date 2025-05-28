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
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare Base here to be shared across models
Base = declarative_base()
