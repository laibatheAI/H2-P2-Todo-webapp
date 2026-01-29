'use client';

import TaskList from '../../../components/TaskList/TaskList';

export default function TasksPage() {
  return (
    <div className="lg:col-span-2 lg:mt-0">
      <div className="px-4 sm:px-0">
        <h3 className="text-xl font-bold leading-6 text-gray-900 mb-2">Your Tasks</h3>
        <p className="text-gray-600 mb-6">
          View and manage your tasks.
        </p>
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200 p-6">
          <TaskList />
        </div>
      </div>
    </div>
  );
}