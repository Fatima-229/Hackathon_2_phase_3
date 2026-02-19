'use client';

import { useState, useEffect, useCallback } from 'react';
import { Task, taskAPI } from '@/utils/taskAPI';
import TaskCard from './TaskCard';

interface TaskListProps {
  filter?: 'all' | 'active' | 'completed';
}

// Skeleton component for loading state
const TaskSkeleton = () => (
  <div className="animate-pulse bg-card rounded-xl p-4 sm:p-6 border border-border">
    <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:space-x-4">
      <div className="h-5 w-5 rounded bg-muted self-start"></div>
      <div className="flex-1 space-y-2">
        <div className="h-4 bg-muted rounded w-3/4"></div>
        <div className="h-3 bg-muted rounded w-1/2"></div>
        <div className="flex flex-wrap gap-2 sm:space-x-2">
          <div className="h-6 w-16 bg-muted rounded-full"></div>
          <div className="h-6 w-20 bg-muted rounded-full"></div>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 sm:space-x-2">
        <div className="h-8 w-16 bg-muted rounded"></div>
        <div className="h-8 w-16 bg-muted rounded"></div>
      </div>
    </div>
  </div>
);

export default function TaskList({ filter = 'all' }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      const tasksData = await taskAPI.getTasks();
      setTasks(tasksData);
    } catch (err) {
      setError('Failed to load tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true; // 'all'
  });

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <TaskSkeleton key={index} />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-10 text-destructive bg-destructive/10 rounded-lg border border-destructive/20 p-4">
        {error}
        <button 
          onClick={fetchTasks}
          className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  const handleTaskUpdate = async (updatedTask: Task) => {
    try {
      const updatedTaskData = await taskAPI.updateTask(updatedTask.id, {
        title: updatedTask.title,
        description: updatedTask.description,
        completed: updatedTask.completed,
        priority: updatedTask.priority,
        due_date: updatedTask.due_date
      });

      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === updatedTaskData.id ? updatedTaskData : task
        )
      );
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleTaskDelete = async (deletedTaskId: string) => {
    try {
      await taskAPI.deleteTask(deletedTaskId);
      setTasks(prevTasks => prevTasks.filter(task => task.id !== deletedTaskId));
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  return (
    <div className="space-y-4">
      {filteredTasks.length === 0 && !loading ? (
        <div className="text-center py-12">
          <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-muted/20 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-foreground mb-1">
            {filter === 'completed'
              ? 'No completed tasks yet'
              : filter === 'active'
                ? 'No active tasks'
                : 'No tasks yet'}
          </h3>
          <p className="text-muted-foreground text-sm sm:text-base">
            {filter === 'completed'
              ? 'Complete some tasks to see them here.'
              : filter === 'active'
                ? 'Great job! All tasks are completed.'
                : 'Get started by creating a new task.'}
          </p>
        </div>
      ) : (
        filteredTasks.map(task => (
          <TaskCard key={task.id} task={task} onTaskUpdate={handleTaskUpdate} onTaskDelete={handleTaskDelete} />
        ))
      )}
    </div>
  );
}