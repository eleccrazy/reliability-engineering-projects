from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from models import Task, TaskCreate, TaskUpdate
from database import SessionLocal, engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Task Management API"}


@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    db = SessionLocal()
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task


@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    db.close()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    db.close()
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    db.close()
    return {"message": "Task deleted"}
