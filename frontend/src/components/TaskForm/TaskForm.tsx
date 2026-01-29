'use client';

import { useState } from 'react';
import { TaskCreateRequest } from '../../../../shared/types/api-contracts';
import { apiClient } from '../../lib/api-client';
import StatusCard from '../StatusCard/StatusCard';

interface TaskFormProps {
  onTaskCreated: (task: any) => void;
  onCancel?: () => void;
}

export default function TaskForm({ onTaskCreated, onCancel }: TaskFormProps) {
  const [formData, setFormData] = useState<Omit<TaskCreateRequest, 'completed'>>({
    title: '',
    description: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [confirmationState, setConfirmationState] = useState<'confirm' | 'success' | 'error'>('confirm');
  const [confirmationMessage, setConfirmationMessage] = useState('');

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

  const handleConfirmCreate = async () => {
    if (!validateForm()) {
      return;
    }

    setSubmitting(true);
    setConfirmationState('confirm');

    try {
      const response = await apiClient.createTask({
        title: formData.title,
        description: formData.description || undefined,
        completed: false
      });

      setConfirmationState('success');
      setConfirmationMessage('Task added successfully');

      // Wait a bit before closing and calling onTaskCreated
      setTimeout(() => {
        onTaskCreated(response.data);
        setFormData({ title: '', description: '' });
        setShowConfirmation(false);
      }, 1500);
    } catch (error: any) {
      setConfirmationState('error');
      setConfirmationMessage(error.message || 'Failed to create task');
      setSubmitting(false);
    }
  };

  const handleCreateClick = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setConfirmationMessage(`Do you want to add this task?\nTitle: ${formData.title}`);
    setShowConfirmation(true);
  };

  return (
    <form onSubmit={handleCreateClick} className="space-y-5">
      <div>
        <label htmlFor="title" className="block text-base font-semibold text-gray-800 dark:text-gray-200 mb-2">
          Title *
        </label>
        <div className="relative">
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className={`mt-1 block w-full px-4 py-3 border ${
              errors.title ? 'border-rose-400' : 'border-gray-300 dark:border-slate-600'
            } rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ${
              errors.title ? 'text-rose-900' : 'text-gray-700 dark:text-white dark:bg-slate-700/50'
            }`}
            placeholder="Enter task title (2–50 characters)"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 rounded-lg blur-sm opacity-0 hover:opacity-20 transition-opacity duration-300 -z-10"></div>
        </div>
        {errors.title && (
          <p className="mt-2 text-sm text-rose-600 dark:text-rose-400 font-medium">{errors.title}</p>
        )}
      </div>

      <div>
        <label htmlFor="description" className="block text-base font-semibold text-gray-800 dark:text-gray-200 mb-2">
          Description
        </label>
        <div className="relative">
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={3}
            className={`mt-1 block w-full px-4 py-3 border ${
              errors.description ? 'border-rose-400' : 'border-gray-300 dark:border-slate-600'
            } rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ${
              errors.description ? 'text-rose-900' : 'text-gray-700 dark:text-white dark:bg-slate-700/50'
            }`}
            placeholder="Enter task description (optional, up to 1000 characters)"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 rounded-lg blur-sm opacity-0 hover:opacity-20 transition-opacity duration-300 -z-10"></div>
        </div>
        {errors.description && (
          <p className="mt-2 text-sm text-rose-600 dark:text-rose-400 font-medium">{errors.description}</p>
        )}
      </div>

      {errors.submit && (
        <div className="relative rounded-xl bg-rose-50 dark:bg-rose-900/20 p-4 border-2 border-rose-200 dark:border-rose-700/50">
          <div className="absolute inset-0 bg-gradient-to-r from-rose-500/10 to-pink-500/10 rounded-xl blur-sm opacity-50 -z-10"></div>
          <p className="text-sm text-rose-800 dark:text-rose-300 font-medium text-center">{errors.submit}</p>
        </div>
      )}

      <div className="flex space-x-4">
        <button
          type="submit"
          disabled={submitting}
          className="relative flex-1 flex justify-center py-3 px-4 border border-transparent text-base font-semibold rounded-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-all duration-200 transform hover:scale-[1.02] hover:shadow-lg hover:shadow-indigo-500/30"
        >
          <span className="relative z-10">{submitting ? 'Creating...' : 'Create Task'}</span>
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="relative flex-1 flex justify-center py-3 px-4 border border-transparent text-base font-semibold rounded-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-[1.02] hover:shadow-lg hover:shadow-indigo-500/30"
          >
            <span className="relative z-10">Cancel</span>
          </button>
        )}
      </div>

      {showConfirmation && (
        <StatusCard
          message={confirmationMessage}
          status={confirmationState}
          onConfirm={confirmationState === 'confirm' ? handleConfirmCreate : undefined}
          onDismiss={() => setShowConfirmation(false)}
          showActions={confirmationState === 'confirm'} type={'confirm'}        />
      )}
    </form>
  );
}