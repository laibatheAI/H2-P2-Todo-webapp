'use client';

import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { Task } from '../../../../shared/types/api-contracts';
import { apiClient } from '../../lib/api-client';
import { authUtils } from '../../lib/auth';
import TaskItem from './TaskItem';
import StatusCard from '../StatusCard/StatusCard';

interface TaskListProps {
  userId?: string;
}

export default function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // Delete confirmation state
  const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);
  const [deleteConfirmationState, setDeleteConfirmationState] = useState<'confirm' | 'success' | 'error'>('confirm');
  const [deleteConfirmationMessage, setDeleteConfirmationMessage] = useState('');
  const [taskToDelete, setTaskToDelete] = useState<{id: string, title: string} | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getTasks();
      setTasks(response.data);
    } catch (err: any) {
      // Don't handle 401 specially here since ProtectedRoute should handle auth status
      // Just show error message
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  // Original delete task function that handles the API call and state update
  const handleDeleteTask = async (taskId: string) => {
    try {
      await apiClient.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
      throw err; // Re-throw so calling function can handle UI state
    }
  };

  const handleDeleteConfirmation = (task: Task) => {
    setTaskToDelete({id: task.id, title: task.title});
    setDeleteConfirmationMessage(`Are you sure you want to delete task "${task.title}"?`);
    setDeleteConfirmationState('confirm');
    setShowDeleteConfirmation(true);
  };

  const handleConfirmDelete = async () => {
    if (!taskToDelete) return;

    setDeleteConfirmationState('confirm');
    try {
      await apiClient.deleteTask(taskToDelete.id);
      // Update the local state to remove the task
      setTasks(tasks.filter(task => task.id !== taskToDelete.id));

      // Update confirmation state to success
      setDeleteConfirmationState('success');
      setDeleteConfirmationMessage('Task deleted successfully');

      // Close the confirmation card after a delay
      setTimeout(() => {
        setShowDeleteConfirmation(false);
        setTaskToDelete(null); // Reset task to delete
      }, 1500);
    } catch (error: any) {
      setDeleteConfirmationState('error');
      setDeleteConfirmationMessage(error.message || 'Failed to delete task');
      setError(error.message || 'Failed to delete task');
      // Close after a delay
      setTimeout(() => {
        setShowDeleteConfirmation(false);
        setTaskToDelete(null);
      }, 1500);
    }
  };

  const handleToggleTask = async (taskId: string) => {
    try {
      const response = await apiClient.toggleTask(taskId);
      setTasks(tasks.map(task =>
        task.id === taskId ? response.data : task
      ));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    }
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task =>
      task.id === updatedTask.id ? updatedTask : task
    ));
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
        {error}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <>
      <div className="relative bg-gradient-to-br from-emerald-teal-50 to-emerald-teal-100 dark:from-slate-800/30 dark:to-slate-700/20 backdrop-blur-sm rounded-2xl border border-emerald-teal-200 dark:border-slate-600/50 shadow-xl shadow-emerald-teal-500/5 hover:shadow-emerald-teal-500/10 transition-all duration-300 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-teal-500/5 to-emerald-teal-500/5 rounded-2xl -z-10"></div>
        <ul className="divide-y divide-gray-200 dark:divide-gray-700/50">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={handleToggleTask}
              onDelete={handleDeleteTask}
              onTaskUpdated={handleTaskUpdated}
              onShowDeleteConfirmation={handleDeleteConfirmation}
            />
          ))}
        </ul>
      </div>

      {showDeleteConfirmation && typeof window !== 'undefined' && createPortal(
        <StatusCard
          message={deleteConfirmationMessage}
          status={deleteConfirmationState}
          onConfirm={deleteConfirmationState === 'confirm' ? handleConfirmDelete : undefined}
          onDismiss={() => {
            setShowDeleteConfirmation(false);
            setTaskToDelete(null);
          } }
          showActions={true} type={'confirm'}        />,
        document.body
      )}
    </>
  );
}