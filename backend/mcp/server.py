"""
MCP Server for Todo Application
Implements the MCP protocol to expose tools for the AI agent
"""
import asyncio
import json
from typing import Dict, Any, Callable
from .tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
)


class MCPServer:
    def __init__(self):
        self.tools: Dict[str, Callable] = {
            "add_task": self._wrap_add_task,
            "list_tasks": self._wrap_list_tasks,
            "complete_task": self._wrap_complete_task,
            "delete_task": self._wrap_delete_task,
            "update_task": self._wrap_update_task
        }
    
    def _wrap_add_task(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for add_task_tool to handle user_id from context"""
        user_id = kwargs.pop('user_id', None)
        if not user_id:
            return {
                "success": False,
                "error": "Missing user_id",
                "message": "User context is required for this operation"
            }
        
        return add_task_tool(user_id, **kwargs)
    
    def _wrap_list_tasks(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for list_tasks_tool to handle user_id from context"""
        user_id = kwargs.pop('user_id', None)
        if not user_id:
            return {
                "success": False,
                "error": "Missing user_id",
                "message": "User context is required for this operation"
            }
        
        return list_tasks_tool(user_id, **kwargs)
    
    def _wrap_complete_task(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for complete_task_tool to handle user_id from context"""
        user_id = kwargs.pop('user_id', None)
        if not user_id:
            return {
                "success": False,
                "error": "Missing user_id",
                "message": "User context is required for this operation"
            }
        
        return complete_task_tool(user_id, **kwargs)
    
    def _wrap_delete_task(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for delete_task_tool to handle user_id from context"""
        user_id = kwargs.pop('user_id', None)
        if not user_id:
            return {
                "success": False,
                "error": "Missing user_id",
                "message": "User context is required for this operation"
            }
        
        return delete_task_tool(user_id, **kwargs)
    
    def _wrap_update_task(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for update_task_tool to handle user_id from context"""
        user_id = kwargs.pop('user_id', None)
        if not user_id:
            return {
                "success": False,
                "error": "Missing user_id",
                "message": "User context is required for this operation"
            }
        
        return update_task_tool(user_id, **kwargs)
    
    def execute_tool(self, tool_name: str, user_id: str, **params) -> Dict[str, Any]:
        """
        Execute a tool with the given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            user_id: ID of the user executing the tool
            **params: Additional parameters for the tool
        
        Returns:
            Result of the tool execution
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "message": f"Tool '{tool_name}' is not available"
            }
        
        # Add user_id to params for the wrapper functions
        params['user_id'] = user_id
        
        try:
            result = self.tools[tool_name](**params)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error executing tool '{tool_name}'"
            }
    
    def get_tool_description(self, tool_name: str) -> Dict[str, Any]:
        """Get description of a tool for the AI agent."""
        descriptions = {
            "add_task": {
                "name": "add_task",
                "description": "Add a new task to the user's task list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Title of the task"},
                        "description": {"type": "string", "description": "Description of the task (optional)"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority level (default: medium)"},
                        "due_date": {"type": "string", "description": "Due date in ISO format (optional)"}
                    },
                    "required": ["title"]
                }
            },
            "list_tasks": {
                "name": "list_tasks",
                "description": "List all tasks for the user, with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "completed": {"type": "boolean", "description": "Filter by completion status (optional)"}
                    }
                }
            },
            "complete_task": {
                "name": "complete_task",
                "description": "Toggle the completion status of a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to toggle"}
                    },
                    "required": ["task_id"]
                }
            },
            "delete_task": {
                "name": "delete_task",
                "description": "Delete a task from the user's task list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            },
            "update_task": {
                "name": "update_task",
                "description": "Update properties of an existing task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to update"},
                        "title": {"type": "string", "description": "New title for the task (optional)"},
                        "description": {"type": "string", "description": "New description for the task (optional)"},
                        "completed": {"type": "boolean", "description": "New completion status (optional)"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "New priority level (optional)"},
                        "due_date": {"type": "string", "description": "New due date in ISO format (optional)"}
                    },
                    "required": ["task_id"]
                }
            }
        }
        
        return descriptions.get(tool_name, {
            "name": tool_name,
            "description": f"Unknown tool: {tool_name}",
            "parameters": {"type": "object", "properties": {}}
        })


# Global MCP server instance
mcp_server = MCPServer()