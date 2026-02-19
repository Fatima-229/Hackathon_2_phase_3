'use client';

import { useState } from 'react';
import { Task, taskAPI } from '@/utils/taskAPI';

interface TaskCardProps {
  task: Task;
  onTaskUpdate: (updatedTask: Task) => void;
  onTaskDelete: (taskId: string) => void;
}

export default function TaskCard({ task, onTaskUpdate, onTaskDelete }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>(task.priority);
  const [dueDate, setDueDate] = useState(task.due_date || '');

  const handleToggleCompletion = async () => {
    try {
      const updatedTask = await taskAPI.toggleTaskCompletion(task.id);
      onTaskUpdate(updatedTask);
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    }
  };

  const handleSaveEdit = async () => {
    try {
      const updatedTask = await taskAPI.updateTask(task.id, {
        title,
        description,
        priority,
        due_date: dueDate || undefined
      });
      onTaskUpdate(updatedTask);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleCancelEdit = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setPriority(task.priority);
    setDueDate(task.due_date || '');
    setIsEditing(false);
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  // Determine priority color
  const priorityColor = task.priority === 'high' ? 'bg-destructive' :
                       task.priority === 'medium' ? 'bg-accent' :
                       'bg-success';

  return (
    <div className={`relative bg-card rounded-xl p-4 sm:p-5 border border-border transition-all duration-200 hover:shadow-lg group ${task.completed ? 'opacity-70' : ''}`}>
      {/* Priority indicator bar */}
      <div className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-xl ${priorityColor}`}></div>

      {isEditing ? (
        <div className="pl-4 space-y-4">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-3 bg-background border border-input rounded-lg text-foreground focus:ring-2 focus:ring-primary focus:border-primary"
            placeholder="Task title"
            autoFocus
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-3 bg-background border border-input rounded-lg text-foreground focus:ring-2 focus:ring-primary focus:border-primary"
            placeholder="Task description"
            rows={3}
          />
          <div className="flex flex-col sm:flex-row sm:flex-wrap gap-3">
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
              className="p-2 bg-background border border-input rounded-lg text-foreground focus:ring-2 focus:ring-primary focus:border-primary flex-grow min-w-[120px]"
            >
              <option value="low" className="bg-card">Low</option>
              <option value="medium" className="bg-card">Medium</option>
              <option value="high" className="bg-card">High</option>
            </select>
            <input
              type="date"
              value={dueDate.split('T')[0]}
              onChange={(e) => setDueDate(e.target.value)}
              className="p-2 bg-background border border-input rounded-lg text-foreground focus:ring-2 focus:ring-primary focus:border-primary flex-grow min-w-[120px]"
            />
          </div>
          <div className="flex flex-col sm:flex-row sm:space-x-3 pt-2 gap-2 sm:gap-0">
            <button
              onClick={handleSaveEdit}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-all duration-200 flex-1 min-w-[100px]"
            >
              Save
            </button>
            <button
              onClick={handleCancelEdit}
              className="px-4 py-2 border border-input text-foreground rounded-lg hover:bg-accent transition-all duration-200 flex-1 min-w-[100px]"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="pl-4">
          <div className="flex flex-col sm:flex-row sm:items-start gap-3">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleCompletion}
              className="mt-1 h-5 w-5 rounded border-input text-primary focus:ring-primary self-start"
            />
            <div className="flex-1 min-w-0">
              <h3 className={`text-base sm:text-lg font-medium truncate ${task.completed ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-2 text-sm sm:text-base text-muted-foreground ${task.completed ? 'line-through' : ''}`}>
                  {task.description}
                </p>
              )}
              <div className="mt-3 flex flex-wrap gap-2">
                <span className={`px-2 py-1 sm:px-2.5 sm:py-1 rounded-full text-xs sm:text-xs font-medium ${
                  task.priority === 'high' ? 'bg-destructive/20 text-destructive border border-destructive/30' :
                  task.priority === 'medium' ? 'bg-accent text-accent-foreground border border-border' :
                  'bg-success/20 text-success border border-success/30'
                }`}>
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </span>
                {task.due_date && (
                  <span className="px-2 py-1 sm:px-2.5 sm:py-1 bg-muted text-muted-foreground rounded-full text-xs sm:text-xs border border-border">
                    Due: {formatDate(task.due_date)}
                  </span>
                )}
              </div>
            </div>
            <div className="flex space-x-2 mt-2 sm:mt-0">
              <button
                onClick={() => setIsEditing(true)}
                className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent transition-all duration-200"
                aria-label="Edit task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                onClick={() => onTaskDelete(task.id)}
                className="p-2 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all duration-200"
                aria-label="Delete task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}