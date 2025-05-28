"""
File: models.py
Description: SQLAlchemy models and Pydantic schemas for task management API.
Author: Gizachew Kassa
Date Created: 2025-05-28
"""

from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String


# SQLAlchemy model
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    completed = Column(String, default="False")


# Pydantic models
class TaskBase(BaseModel):
    name: str
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: str | None = None
    completed: bool | None = None


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
