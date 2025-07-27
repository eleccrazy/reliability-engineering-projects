"""
File: main.py
Description: FastAPI application for task management with CRUD operations.
Author: Gizachew Kassa
Date Created: 2025-05-28
"""

from typing import List

from database import Base, SessionLocal, engine
from db_models import TaskDB
from fastapi import FastAPI, HTTPException, status
from schemas import Task, TaskCreate, TaskUpdate
from sqlalchemy.exc import OperationalError

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Task Management API"}


# Add a /health endpoint for health checks
@app.get("/health", tags=["Health"])
def health():
    db = SessionLocal()
    try:
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except OperationalError:
        raise HTTPException(
            status_code=503, detail={"status": "error", "database": "unreachable"}
        )
    finally:
        db.close()


@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    db = SessionLocal()
    db_task = TaskDB(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task


@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    db = SessionLocal()
    tasks = db.query(TaskDB).all()
    db.close()
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    db = SessionLocal()
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    db.close()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    db = SessionLocal()
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task is None:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    db.close()
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task is None:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    db.close()
    return {"message": "Task deleted"}
