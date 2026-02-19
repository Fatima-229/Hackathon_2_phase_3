"""
MCP Tools for Todo Application
These tools connect to existing task operations in the backend
"""
import json
from typing import Dict, Any
from sqlmodel import Session, select
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
from database import get_session


def add_task_tool(user_id: str, title: str, description: str = None, priority: str = "medium", due_date: str = None) -> Dict[str, Any]:
    """Add a new task for the user."""
    try:
        with next(get_session()) as session:
            # Prepare task data
            task_data = {
                "title": title,
                "description": description,
                "priority": priority
            }
            
            if due_date:
                from datetime import datetime
                task_data["due_date"] = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            
            # Create task
            task_create = TaskCreate(**task_data)
            task_dict = task_create.model_dump()
            task_dict['user_id'] = user_id  # Override user_id to ensure security
            
            db_task = Task(**task_dict)
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            
            return {
                "success": True,
                "task_id": str(db_task.id),
                "message": f"Task '{db_task.title}' added successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to add task"
        }


def list_tasks_tool(user_id: str, completed: bool = None) -> Dict[str, Any]:
    """List tasks for the user with optional filtering."""
    try:
        with next(get_session()) as session:
            # Build query
            query = select(Task).where(Task.user_id == user_id)
            
            if completed is not None:
                query = query.where(Task.completed == completed)
                
            tasks = session.exec(query).all()
            
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                })
            
            return {
                "success": True,
                "tasks": task_list,
                "count": len(task_list),
                "message": f"Retrieved {len(task_list)} tasks"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to list tasks"
        }


def complete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """Toggle completion status of a task."""
    try:
        with next(get_session()) as session:
            # Get the task
            task = session.get(Task, task_id)
            
            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found"
                }
            
            # Verify user owns the task
            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Not authorized",
                    "message": "Not authorized to update this task"
                }
            
            # Toggle completion status
            task.completed = not task.completed
            from datetime import datetime
            task.updated_at = datetime.utcnow()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            status = "completed" if task.completed else "marked incomplete"
            return {
                "success": True,
                "task_id": str(task.id),
                "completed": task.completed,
                "message": f"Task '{task.title}' {status}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update task completion status"
        }


def delete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """Delete a task."""
    try:
        with next(get_session()) as session:
            # Get the task
            task = session.get(Task, task_id)
            
            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found"
                }
            
            # Verify user owns the task
            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Not authorized",
                    "message": "Not authorized to delete this task"
                }
            
            # Delete the task
            session.delete(task)
            session.commit()
            
            return {
                "success": True,
                "task_id": str(task.id),
                "message": f"Task '{task.title}' deleted successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to delete task"
        }


def update_task_tool(user_id: str, task_id: str, title: str = None, description: str = None, 
                     completed: bool = None, priority: str = None, due_date: str = None) -> Dict[str, Any]:
    """Update a task."""
    try:
        with next(get_session()) as session:
            # Get the task
            task = session.get(Task, task_id)
            
            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found"
                }
            
            # Verify user owns the task
            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Not authorized",
                    "message": "Not authorized to update this task"
                }
            
            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if completed is not None:
                update_data["completed"] = completed
            if priority is not None:
                update_data["priority"] = priority
            if due_date is not None:
                from datetime import datetime
                update_data["due_date"] = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            
            # Update task fields
            for field, value in update_data.items():
                setattr(task, field, value)
            
            # Update the timestamp
            from datetime import datetime
            task.updated_at = datetime.utcnow()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "success": True,
                "task_id": str(task.id),
                "message": f"Task '{task.title}' updated successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update task"
        }