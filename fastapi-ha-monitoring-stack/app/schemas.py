"""
File: schemas.py
Description: Pydantic models for task management API, defining data validation and serialization.
Author: Gizachew Kassa
Date Created: 2025-05-28
"""

from pydantic import BaseModel, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)
