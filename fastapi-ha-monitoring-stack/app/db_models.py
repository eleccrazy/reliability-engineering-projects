"""
File: db_models.py
Description: SQLAlchemy models for task management API.
Author: Gizachew Kassa
Date Created: 2025-05-29
"""

from database import Base
from sqlalchemy import Column, Integer, String


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    completed = Column(String, default="False")
