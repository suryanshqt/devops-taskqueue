from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Task
from schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("")
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return {
        "success": True,
        "count": len(tasks),
        "data": [TaskResponse.model_validate(task) for task in tasks],
    }


@router.post("", status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task.title.strip(), description=task.description.strip())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return {
        "success": True,
        "message": "Task created successfully",
        "data": TaskResponse.model_validate(db_task),
    }


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"success": True, "message": "Task deleted successfully"}
