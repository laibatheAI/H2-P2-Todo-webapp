'use client';

import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { Task, TaskUpdateRequest } from '../../../../shared/types/api-contracts';
import { apiClient } from '../../lib/api-client';
import StatusCard from '../StatusCard/StatusCard';

interface TaskUpdateFormProps {
  task: Task;
  onTaskUpdated: (task: Task) => void;
  onCancel: () => void;
}

export default function TaskUpdateForm({ task, onTaskUpdated, onCancel }: TaskUpdateFormProps) {
  const [formData, setFormData] = useState<{
    title: string;
    description?: string;
  }>({
    title: task.title ?? '',
    description: task.description || ''
  });
  const [completed, setCompleted] = useState(task.completed);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [showUpdateConfirmation, setShowUpdateConfirmation] = useState(false);
  const [updateConfirmationState, setUpdateConfirmationState] = useState<'confirm' | 'success' | 'error'>('confirm');
  const [updateConfirmationMessage, setUpdateConfirmationMessage] = useState('');

  useEffect(() => {
    setFormData({
      title: task.title ?? '',
      description: task.description || ''
    });
    setCompleted(task.completed);
  }, [task]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleCompletedChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCompleted(e.target.checked);
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Title validation (2-50 characters)
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length < 2) {
      newErrors.title = 'Title must be at least 2 characters';
    } else if (formData.title.length > 50) {
      newErrors.title = 'Task title should be in 2 to 50 characters';
    }

    // Description validation (max 1000 characters)
    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be less than 1000 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleConfirmUpdate = async () => {
    if (!validateForm()) {
      return;
    }

    setSubmitting(true);
    setUpdateConfirmationState('confirm');

    try {
      const response = await apiClient.updateTask(task.id, {
        title: formData.title,
        description: formData.description || undefined,
        completed: completed
      });

      setUpdateConfirmationState('success');
      setUpdateConfirmationMessage('Task updated successfully');

      // Wait a bit before closing and calling onTaskUpdated
      setTimeout(() => {
        onTaskUpdated(response.data);
        setShowUpdateConfirmation(false);
      }, 1500);
    } catch (error: any) {
      setUpdateConfirmationState('error');
      setUpdateConfirmationMessage(error.message || 'Failed to update task');
      setSubmitting(false);
    }
  };

  const handleUpdateClick = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setUpdateConfirmationMessage(`Do you want to update this task?\nTitle: ${formData.title}`);
    setShowUpdateConfirmation(true);
  };

  return (
    <>
      <form onSubmit={handleUpdateClick} className="space-y-4 p-3 bg-gray-50 rounded-md">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Title *
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className={`mt-1 block w-full px-3 py-2 border ${
              errors.title ? 'border-red-300' : 'border-gray-300'
            } rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm`}
            placeholder="Enter task title (2–50 characters)"
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-600">{errors.title}</p>
          )}
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={3}
            className={`mt-1 block w-full px-3 py-2 border ${
              errors.description ? 'border-red-300' : 'border-gray-300'
            } rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm`}
            placeholder="Enter task description (optional, up to 1000 characters)"
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description}</p>
          )}
        </div>

        <div className="flex items-center">
          <input
            id="completed"
            name="completed"
            type="checkbox"
            checked={completed}
            onChange={handleCompletedChange}
            className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
          />
          <label htmlFor="completed" className="ml-2 block text-sm text-gray-900">
            Mark as completed
          </label>
        </div>

        {errors.submit && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">{errors.submit}</h3>
              </div>
            </div>
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
          <button
            type="submit"
            disabled={submitting}
            className="flex-1 inline-flex justify-center py-2 px-3 border border-transparent text-sm font-medium rounded-md text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 shadow-sm"
          >
            {submitting ? 'Updating...' : 'Update Task'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 inline-flex justify-center py-2 px-3 border border-transparent text-sm font-medium rounded-md text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-sm"
          >
            Cancel
          </button>
        </div>
      </form>

      {showUpdateConfirmation && typeof window !== 'undefined' && createPortal(
        <StatusCard
          message={updateConfirmationMessage}
          status={updateConfirmationState}
          onConfirm={updateConfirmationState === 'confirm' ? handleConfirmUpdate : undefined}
          onDismiss={() => setShowUpdateConfirmation(false)}
          showActions={true} type={'confirm'}        />,
        document.body
      )}
    </>
  );
}