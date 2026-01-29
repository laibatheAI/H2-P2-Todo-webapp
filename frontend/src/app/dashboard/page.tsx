'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Task, User } from '../../../../shared/types/api-contracts';
import { apiClient } from '../../lib/api-client';
import { authUtils } from '../../lib/auth';
import TaskForm from '../../components/TaskForm/TaskForm';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    pending: 0,
    completionRate: 0
  });
  const [recentTasks, setRecentTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Get user from local storage
        const userData = authUtils.getUser();
        if (userData) {
          setUser(userData);
        }

        // Fetch tasks and calculate stats
        const response = await apiClient.getTasks();
        const tasks = response.data;

        // Calculate stats
        const total = tasks.length;
        const completed = tasks.filter((task: Task) => task.completed).length;
        const pending = total - completed;
        const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

        setStats({
          total,
          completed,
          pending,
          completionRate
        });

        // Get recent 5 tasks (most recent first)
        const sortedTasks = [...tasks].sort((a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        ).slice(0, 5);

        setRecentTasks(sortedTasks);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Redirect to login if unauthorized
        if ((error as any).response?.status === 401) {
          authUtils.logout();
          router.push('/');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [router]);

  const handleTaskCreated = (newTask: any) => {
    // Refresh dashboard data after task creation
    // Use router refresh instead of window.location.reload to avoid auth issues
    router.refresh();
  };

  const handleTaskClick = (taskId: string) => {
    router.push(`/dashboard/tasks/${taskId}`);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="text-center">
        <h1 className=" text-3xl font-bold text-indigo-600 dark:text-white">
          Welcome back, {user?.name}!
        </h1>
        <p className="mt-2 text-gray-700 dark:text-gray-300">
          Here's what's happening with your tasks today.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Tasks Card */}
        <div className="relative bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-2xl p-6 border border-blue-200 dark:border-blue-700/30 shadow-lg shadow-blue-500/10 hover:shadow-blue-500/20 transition-all duration-300 hover:scale-[1.02] backdrop-blur-sm">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-blue-300/5 rounded-2xl -z-10"></div>
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/20 to-blue-300/20 rounded-2xl blur opacity-0 hover:opacity-30 transition-opacity duration-300 -z-10"></div>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="relative w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-blue-600 rounded-xl blur-sm opacity-50"></div>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white relative z-10" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-blue-800 dark:text-blue-300">Total Tasks</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{stats.total}</p>
            </div>
          </div>
        </div>

        {/* Completed Tasks Card */}
        <div className="relative bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-2xl p-6 border border-green-200 dark:border-green-700/30 shadow-lg shadow-green-500/10 hover:shadow-green-500/20 transition-all duration-300 hover:scale-[1.02] backdrop-blur-sm">
          <div className="absolute inset-0 bg-gradient-to-r from-green-500/5 to-green-300/5 rounded-2xl -z-10"></div>
          <div className="absolute -inset-1 bg-gradient-to-r from-green-500/20 to-green-300/20 rounded-2xl blur opacity-0 hover:opacity-30 transition-opacity duration-300 -z-10"></div>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="relative w-10 h-10 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg shadow-green-500/30">
                <div className="absolute inset-0 bg-gradient-to-br from-green-400 to-green-600 rounded-xl blur-sm opacity-50"></div>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white relative z-10" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-green-800 dark:text-green-300">Completed</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{stats.completed}</p>
            </div>
          </div>
        </div>

        {/* Pending Tasks Card */}
        <div className="relative bg-gradient-to-br from-yellow-50 to-yellow-100 dark:from-yellow-900/20 dark:to-yellow-800/20 rounded-2xl p-6 border border-yellow-200 dark:border-yellow-700/30 shadow-lg shadow-yellow-500/10 hover:shadow-yellow-500/20 transition-all duration-300 hover:scale-[1.02] backdrop-blur-sm">
          <div className="absolute inset-0 bg-gradient-to-r from-yellow-500/5 to-yellow-300/5 rounded-2xl -z-10"></div>
          <div className="absolute -inset-1 bg-gradient-to-r from-yellow-500/20 to-yellow-300/20 rounded-2xl blur opacity-0 hover:opacity-30 transition-opacity duration-300 -z-10"></div>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="relative w-10 h-10 bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-xl flex items-center justify-center shadow-lg shadow-yellow-500/30">
                <div className="absolute inset-0 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-xl blur-sm opacity-50"></div>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white relative z-10" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-yellow-800 dark:text-yellow-300">Pending</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{stats.pending}</p>
            </div>
          </div>
        </div>

        {/* Completion Rate Card */}
        <div className="relative bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-2xl p-6 border border-purple-200 dark:border-purple-700/30 shadow-lg shadow-purple-500/10 hover:shadow-purple-500/20 transition-all duration-300 hover:scale-[1.02] backdrop-blur-sm">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-purple-300/5 rounded-2xl -z-10"></div>
          <div className="absolute -inset-1 bg-gradient-to-r from-purple-500/20 to-purple-300/20 rounded-2xl blur opacity-0 hover:opacity-30 transition-opacity duration-300 -z-10"></div>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="relative w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/30">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-400 to-purple-600 rounded-xl blur-sm opacity-50"></div>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white relative z-10" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                </svg>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-purple-800 dark:text-purple-300">Completion Rate</p>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{stats.completionRate}%</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Tasks Section */}
        <div className="relative bg-gradient-to-br from-gray-50 to-gray-100 dark:from-slate-800/30 dark:to-slate-700/20 backdrop-blur-sm rounded-2xl border border-gray-200 dark:border-slate-600/50 shadow-xl shadow-indigo-500/5 hover:shadow-indigo-500/10 transition-all duration-300 p-6">
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 rounded-2xl -z-10"></div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Recent Tasks</h2>
            <button
              onClick={() => router.push('/dashboard/tasks')}
              className="relative px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 hover:scale-105 bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/40"
            >
              <span className="relative z-10">View All</span>
            </button>
          </div>

          {recentTasks.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">No tasks yet. Create your first task!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {recentTasks.map((task) => (
                <div
                  key={task.id}
                  onClick={() => handleTaskClick(task.id)}
                  className="relative p-5 rounded-xl bg-white/50 dark:bg-slate-700/30 backdrop-blur-sm border border-gray-200 dark:border-slate-600/50 hover:bg-indigo-500/10 hover:border-indigo-500/30 cursor-pointer transition-all duration-300 group hover:shadow-lg hover:shadow-indigo-500/10 hover:-translate-y-0.5"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 rounded-xl -z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 dark:text-white truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-300 transition-colors duration-300">
                        {task.title}
                      </h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
                        {task.description || 'No description'}
                      </p>
                      <div className="mt-3 flex items-center space-x-4">
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium transition-all duration-300 ${
                          task.completed
                            ? 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-800 dark:text-green-300 border border-green-500/30 shadow-sm shadow-green-500/10'
                            : 'bg-gradient-to-r from-yellow-500/20 to-amber-500/20 text-yellow-800 dark:text-yellow-300 border border-yellow-500/30 shadow-sm shadow-yellow-500/10'
                        }`}>
                          {task.completed ? 'Completed' : 'Pending'}
                        </span>
                        <span className="text-xs text-gray-500 dark:text-gray-400 transition-colors duration-300">
                          {new Date(task.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    <div className="ml-4 flex-shrink-0 transition-transform duration-300 group-hover:translate-x-1">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400 group-hover:text-indigo-500 transition-colors duration-300" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Actions / Create Task Section */}
        <div>
          <div className="relative bg-gradient-to-br from-gray-50 to-gray-100 dark:from-slate-800/30 dark:to-slate-700/20 backdrop-blur-sm rounded-2xl border border-gray-200 dark:border-slate-600/50 shadow-xl shadow-indigo-500/5 hover:shadow-indigo-500/10 transition-all duration-300 p-6 mb-6">
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 rounded-2xl -z-10"></div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Quick Actions</h2>
            <div className="grid grid-cols-1 gap-4">
              <button
                onClick={() => router.push('/dashboard/tasks/create')}
                className="relative flex items-center justify-center px-6 py-4 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg hover:shadow-indigo-500/30"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="-ml-1 mr-3 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Create New Task
              </button>

              <button
                onClick={() => router.push('/dashboard/tasks')}
                className="relative flex items-center justify-center px-6 py-4 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg hover:shadow-indigo-500/30"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="-ml-1 mr-3 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                  <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                </svg>
                View All Tasks
              </button>
            </div>
          </div>

          {/* Create Task Form */}
          <div className="relative bg-gradient-to-br from-gray-50 to-gray-100 dark:from-slate-800/30 dark:to-slate-700/20 backdrop-blur-sm rounded-2xl border border-gray-200 dark:border-slate-600/50 shadow-xl shadow-indigo-500/5 hover:shadow-indigo-500/10 transition-all duration-300 p-6">
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 rounded-2xl -z-10"></div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Create New Task</h3>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Add a new task to your list.
            </p>
            <TaskForm onTaskCreated={handleTaskCreated} />
          </div>
        </div>
      </div>
    </div>
  );
}