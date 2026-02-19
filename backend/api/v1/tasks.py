from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from database import get_session
from models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from models.user import User
from utils.auth import get_current_user
from datetime import datetime


router = APIRouter()


@router.get("/", response_model=List[TaskPublic])
def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, regex="^(low|medium|high)$", description="Filter by priority"),
    limit: int = Query(100, ge=1, le=100, description="Limit number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get all tasks for the authenticated user with optional filtering.
    """
    # Start with base query filtered by user
    query = select(Task).where(Task.user_id == current_user.id)
    
    # Apply filters if provided
    if completed is not None:
        query = query.where(Task.completed == completed)
    
    if priority is not None:
        query = query.where(Task.priority == priority)
    
    # Apply pagination
    query = query.offset(offset).limit(limit)
    
    tasks = session.exec(query).all()
    return tasks


@router.post("/", response_model=TaskPublic)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Ensure the task is assigned to the current user
    task_dict = task.model_dump()
    task_dict['user_id'] = current_user.id  # Override user_id to ensure security
    task_dict['id'] = None  # Ensure a new ID is generated
    task_dict['created_at'] = datetime.utcnow()
    task_dict['updated_at'] = datetime.utcnow()
    
    db_task = Task(**task_dict)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task


@router.get("/{task_id}", response_model=TaskPublic)
def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    """
    task = session.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Ensure user owns the task
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    
    return task


@router.put("/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID.
    """
    db_task = session.get(Task, task_id)
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Ensure user owns the task
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    # Update the timestamp
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task


@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID.
    """
    task = session.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Ensure user owns the task
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    session.delete(task)
    session.commit()
    
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete", response_model=TaskPublic)
def toggle_task_completion(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task.
    """
    task = session.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Ensure user owns the task
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task