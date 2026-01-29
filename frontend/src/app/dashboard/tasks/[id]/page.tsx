'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Task } from '@shared/types/api-contracts';
import { apiClient } from '../../../../lib/api-client';
import { authUtils } from '../../../../lib/auth';
import TaskUpdateForm from '../../../../components/TaskForm/TaskUpdateForm';

export default function TaskDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        setLoading(true);
        const response = await apiClient.getTask(id as string);
        setTask(response.data);
      } catch (err: any) {
        setError(err.message || 'Failed to load task');
        if (err.response?.status === 401) {
          authUtils.logout();
          router.push('/');
        }
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchTask();
    }
  }, [id, router]);

  const handleToggle = async () => {
    if (!task) return;

    try {
      const response = await apiClient.toggleTask(task.id);
      setTask(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    }
  };

  const handleDelete = async () => {
    if (!task || !window.confirm(`Are you sure you want to delete task "${task.title}"?`)) {
      return;
    }

    try {
      await apiClient.deleteTask(task.id);
      router.push('/dashboard/tasks');
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    }
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTask(updatedTask);
    setIsEditing(false);
  };

  const handleEditCancel = () => {
    setIsEditing(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
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

  if (!task) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Task not found.</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white dark:bg-slate-800/50 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200 dark:border-slate-700 p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Task Details</h1>
          <button
            onClick={() => router.back()}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-slate-700 rounded-lg hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors duration-200"
          >
            Back
          </button>
        </div>

        {isEditing ? (
          <TaskUpdateForm
            task={task}
            onTaskUpdated={handleTaskUpdated}
            onCancel={handleEditCancel}
          />
        ) : (
          <div className="space-y-6">
            <div className="flex items-start">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={handleToggle}
                className="h-6 w-6 text-emerald-teal-600 border-gray-300 rounded focus:ring-emerald-teal-500 focus:ring-2 mt-1"
              />
              <div className="ml-4 flex-1">
                <h2 className={`text-xl font-bold ${
                  task.completed ? 'text-gray-500 line-through' : 'text-gray-900 dark:text-white'
                }`}>
                  {task.title}
                </h2>
                {task.description && (
                  <p className={`mt-3 text-gray-600 dark:text-gray-300 ${
                    task.completed ? 'text-gray-400' : ''
                  }`}>
                    {task.description}
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-50 dark:bg-slate-700/50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Status</h3>
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  task.completed
                    ? 'bg-emerald-teal-100 text-emerald-teal-800 dark:bg-emerald-teal-800/30 dark:text-emerald-teal-300'
                    : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800/30 dark:text-yellow-300'
                }`}>
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
              </div>

              <div className="bg-gray-50 dark:bg-slate-700/50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Created</h3>
                <p className="text-gray-900 dark:text-white">
                  {new Date(task.created_at).toLocaleString()}
                </p>
              </div>

              <div className="bg-gray-50 dark:bg-slate-700/50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">ID</h3>
                <p className="text-gray-900 dark:text-white font-mono text-sm">
                  {task.id}
                </p>
              </div>

              <div className="bg-gray-50 dark:bg-slate-700/50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Updated</h3>
                <p className="text-gray-900 dark:text-white">
                  {new Date(task.updated_at).toLocaleString()}
                </p>
              </div>
            </div>

            <div className="flex flex-wrap gap-3 pt-4">
              <button
                onClick={handleToggle}
                className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                  task.completed
                    ? 'text-emerald-teal-700 bg-emerald-teal-100 hover:bg-emerald-teal-200 dark:text-emerald-teal-300 dark:bg-emerald-teal-900/30 dark:hover:bg-emerald-teal-800/50'
                    : 'text-emerald-teal-700 bg-emerald-teal-100 hover:bg-emerald-teal-200 dark:text-emerald-teal-300 dark:bg-emerald-teal-900/30 dark:hover:bg-emerald-teal-800/50'
                }`}
              >
                {task.completed ? 'Mark as Pending' : 'Mark as Completed'}
              </button>

              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 text-sm font-medium text-white bg-emerald-teal-500 hover:bg-emerald-teal-600 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-emerald-teal-500 focus:ring-opacity-50"
              >
                Edit Task
              </button>

              <button
                onClick={handleDelete}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors duration-200"
              >
                Delete Task
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}