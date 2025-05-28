"""
File: conftest.py
Description: Configuration for pytest to set up the FastAPI test client and database connection.
Author: Gizachew Kassa
Date Created: 2025-05-28
"""

import os

import pytest
from database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use the env variable (already exported in your shell)
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Setup test engine and session
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create fresh schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# TestClient fixture
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
