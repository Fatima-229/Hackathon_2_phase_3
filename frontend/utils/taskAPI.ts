// utils/taskAPI.ts
import { fetchClient } from './fetchClient';
import { API_BASE_URL } from '../constants/api';

const TASKS_API_URL = `${API_BASE_URL}/tasks`; // GET all tasks


export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
}

export const taskAPI = {
  // Get all tasks for the authenticated user
  getTasks: async (): Promise<Task[]> => {
    try {
      const response = await fetchClient(TASKS_API_URL);
      if (!response.ok) {
        if (response.status === 401) {
          // Don't throw error for 401, let the fetchClient handle it
          return [];
        }
        throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  // Get a specific task by ID
  getTaskById: async (id: string): Promise<Task> => {
    try {
      const response = await fetchClient(`${TASKS_API_URL}/${id}`);
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication required');
        }
        throw new Error(`Failed to fetch task: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching task:', error);
      throw error;
    }
  },

  // Create a new task
  createTask: async (taskData: CreateTaskData): Promise<Task> => {
    try {
      const response = await fetchClient(TASKS_API_URL, {
        method: 'POST',
        body: JSON.stringify(taskData),
      });
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication required');
        }
        throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  // Update a task
  updateTask: async (id: string, taskData: UpdateTaskData): Promise<Task> => {
    try {
      const response = await fetchClient(`${TASKS_API_URL}/${id}`, {
        method: 'PUT',
        body: JSON.stringify(taskData),
      });
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication required');
        }
        throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  },

  // Delete a task
  deleteTask: async (id: string): Promise<void> => {
    try {
      const response = await fetchClient(`${TASKS_API_URL}/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication required');
        }
        throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  },

  // Toggle task completion status
  toggleTaskCompletion: async (id: string): Promise<Task> => {
    try {
      const response = await fetchClient(`${TASKS_API_URL}/${id}/complete`, {
        method: 'PATCH',
      });
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication required');
        }
        throw new Error(`Failed to toggle task completion: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  },
};