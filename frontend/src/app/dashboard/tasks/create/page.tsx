'use client';

import { useRouter } from 'next/navigation';
import { TaskCreateRequest } from '../../../../../../shared/types/api-contracts';
import { apiClient } from '../../../../lib/api-client';
import { authUtils } from '../../../../lib/auth';
import TaskForm from '../../../../components/TaskForm/TaskForm';

export default function CreateTaskPage() {
  const router = useRouter();

  const handleTaskCreated = (createdTask: any) => {
    // Navigate back to the dashboard after successful task creation
    router.push('/dashboard');
  };

  const handleCancel = () => {
    router.back();
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white dark:bg-slate-800/50 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200 dark:border-slate-700 p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Create New Task</h1>
          <button
            onClick={handleCancel}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-slate-700 rounded-lg hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-emerald-teal-500 focus:ring-opacity-50"
          >
            Cancel
          </button>
        </div>

        <TaskForm
          onTaskCreated={handleTaskCreated}
          onCancel={handleCancel}
        />
      </div>
    </div>
  );
}