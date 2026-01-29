'use client';

import { useState } from 'react';
import { createPortal } from 'react-dom';
import { Task } from '../../../../shared/types/api-contracts';
import TaskUpdateForm from '../TaskForm/TaskUpdateForm';
import StatusCard from '../StatusCard/StatusCard';

interface TaskItemProps {
  task: Task;
  onToggle: (taskId: string) => void;
  onDelete: (taskId: string) => void;
  onTaskUpdated: (task: Task) => void;
  onShowDeleteConfirmation: (task: Task) => void;
}

export default function TaskItem({ task, onToggle, onDelete, onTaskUpdated, onShowDeleteConfirmation }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  const handleToggle = () => {
    onToggle(task.id);
  };

  const handleDeleteClick = () => {
    onShowDeleteConfirmation(task);
  };

  // Removed handleConfirmDelete as it's now handled at TaskList level

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleUpdateCancel = () => {
    setIsEditing(false);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    onTaskUpdated(updatedTask);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="relative px-2 py-3 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl m-2 border border-blue-200 dark:border-blue-700/50">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-indigo-500/10 rounded-xl -z-10"></div>
        <TaskUpdateForm
          task={task}
          onTaskUpdated={handleTaskUpdated}
          onCancel={handleUpdateCancel}
        />
      </div>
    );
  }

  return (
    <>
      <li className="relative px-6 py-5 bg-white/30 dark:bg-slate-700/30 backdrop-blur-sm border border-gray-200 dark:border-slate-600/50 rounded-xl m-1 hover:bg-indigo-500/10 hover:border-indigo-500/30 transition-all duration-300 group hover:shadow-lg hover:shadow-indigo-500/10 hover:-translate-y-0.5">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 rounded-xl -z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <div className="flex flex-col gap-3">
          <div className="flex justify-end space-x-2">
            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium transition-all duration-300 ${
              task.completed
                ? 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-800 dark:text-green-300 border border-green-500/30 shadow-sm shadow-green-500/10'
                : 'bg-gradient-to-r from-yellow-500/20 to-amber-500/20 text-yellow-800 dark:text-yellow-300 border border-yellow-500/30 shadow-sm shadow-yellow-500/10'
            }`}>
              {task.completed ? 'Completed' : 'Pending'}
            </span>
            <button
              onClick={handleEdit}
              className="relative p-1.5 text-gray-500 hover:text-white hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-600 rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <svg className="h-4 w-4 relative z-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
            </button>
            <button
              onClick={handleDeleteClick}
              disabled={isDeleting}
              className="relative p-1.5 text-gray-500 hover:text-white hover:bg-gradient-to-r hover:from-red-600 hover:to-rose-600 rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
            >
              {isDeleting ? (
                <svg className="animate-spin h-4 w-4 relative z-10" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="h-4 w-4 relative z-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          </div>
          <div className="flex items-center min-w-0">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggle}
              className="h-6 w-6 text-indigo-600 bg-white dark:bg-slate-700 border-gray-300 rounded focus:ring-indigo-500 focus:ring-2 transition-all duration-200 hover:scale-110"
            />
            <div className="ml-4 min-w-0 flex-1">
              <p className={`text-base font-semibold transition-colors duration-300 ${
                task.completed ? 'text-gray-500 line-through' : 'text-gray-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-300'
              }`}>
                {task.title}
              </p>
              {task.description && (
                <p className={`text-sm mt-1 transition-colors duration-300 ${
                  task.completed ? 'text-gray-400' : 'text-gray-600 dark:text-gray-400'
                }`}>
                  {task.description}
                </p>
              )}
            </div>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between">
          <div className="text-sm text-gray-500 dark:text-gray-400 transition-colors duration-300">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400 transition-colors duration-300">
            ID: {task.id.substring(0, 8)}...
          </div>
        </div>
      </li>

    </>
  );
}