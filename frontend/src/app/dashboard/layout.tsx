'use client';

import { useState, useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { authUtils } from '../../lib/auth';
import { apiClient } from '../../lib/api-client';
import ProtectedRoute from '../../components/Auth/ProtectedRoute';
import { User } from '../../../../shared/types/api-contracts';

export default function DashboardLayout({
  children
}: {
  children: React.ReactNode;
}) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    // Get user data from local storage
    const userData = authUtils.getUser();
    if (userData) {
      setUser(userData);
    }
    setLoading(false);

    // Check for saved dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(savedDarkMode);
    if (savedDarkMode) {
      document.documentElement.classList.add('dark');
    }
  }, []);

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem('darkMode', String(newDarkMode));
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-slate-900' : 'bg-gradient-to-br from-gray-50 via-indigo-50 to-gray-50'}`}>
        {/* Top Navbar */}
        <nav className={`sticky top-0 z-10 transition-colors duration-300 ${darkMode ? 'bg-slate-800' : 'bg-white'} backdrop-blur-lg border-b ${darkMode ? 'border-slate-700' : 'border-gray-200'}`}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <h1 className={`text-2xl font-bold ${darkMode ? 'text-indigo-400' : 'text-indigo-600'} tracking-tight`}>TaskNest</h1>
              </div>

              <div className="flex items-center space-x-6">
                {/* Desktop Navigation - Hidden on mobile */}
                <div className="hidden md:flex space-x-6">
                  <button
                    onClick={() => router.push('/dashboard')}
                    className={`font-medium transition-colors duration-200 ${
                      pathname === '/dashboard/tasks/create'
                        ? darkMode
                          ? 'text-indigo-300 border-b-2 border-indigo-300 pb-1'
                          : 'text-indigo-600 border-b-2 border-indigo-600 pb-1'
                        : darkMode
                          ? 'text-gray-300 hover:text-purple-400'
                          : 'text-gray-700 hover:text-indigo-600'
                    }`}
                  >
                    Dashboard
                  </button>

                  <button
                    onClick={() => router.push('/dashboard/tasks/create')}
                    className={`font-medium transition-colors duration-200 ${
                      pathname === '/dashboard/tasks/create'
                        ? darkMode
                          ? 'text-indigo-300 border-b-2 border-indigo-300 pb-1'
                          : 'text-indigo-600 border-b-2 border-indigo-600 pb-1'
                        : darkMode
                          ? 'text-gray-300 hover:text-purple-400'
                          : 'text-gray-700 hover:text-indigo-600'
                    }`}
                  >
                    Create Task
                  </button>
                </div>

                {/* Mobile Controls - Only visible on mobile */}
                <div className="md:hidden flex items-center space-x-4">
                  {/* Dark mode toggle */}
                  <button
                    onClick={toggleDarkMode}
                    className={`p-2 rounded-full transition-colors duration-200 ${
                      darkMode ? 'text-yellow-400 hover:bg-slate-700' : 'text-gray-700 hover:bg-gray-200'
                    }`}
                    aria-label="Toggle dark mode"
                  >
                    {darkMode ? (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                      </svg>
                    )}
                  </button>

                  <button
                    onClick={() => setMobileMenuOpen(true)}
                    className={`p-2 rounded-lg transition-colors duration-200 ${
                      darkMode
                        ? 'text-gray-300 hover:bg-slate-700'
                        : 'text-gray-700 hover:bg-gray-200'
                    }`}
                    aria-label="Open menu"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
                </div>

                {/* Desktop Controls - Hidden on mobile */}
                <div className="hidden md:flex items-center space-x-4">
                  {/* Logout Button */}
                  <button
                    onClick={async () => {
                      try {
                        await apiClient.logout();
                      } catch (error) {
                        console.error('Logout error:', error);
                        // Continue with logout even if API call fails
                      } finally {
                        authUtils.logout();
                        window.location.href = '/';
                      }
                    }}
                    className={`p-2 rounded-lg transition-colors duration-200 ${
                      darkMode
                        ? 'text-red-400 hover:bg-slate-700 hover:text-red-300'
                        : 'text-red-600 hover:bg-gray-200 hover:text-red-700'
                    }`}
                    aria-label="Logout"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                  </button>

                  {/* Dark mode toggle */}
                  <button
                    onClick={toggleDarkMode}
                    className={`p-2 rounded-full transition-colors duration-200 ${
                      darkMode ? 'text-yellow-400 hover:bg-slate-700' : 'text-gray-700 hover:bg-gray-200'
                    }`}
                    aria-label="Toggle dark mode"
                  >
                    {darkMode ? (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Mobile Menu Slide-in Panel */}
        {mobileMenuOpen && (
          <div className="fixed inset-0 z-50 overflow-hidden md:hidden">
            <div
              className="absolute inset-0 bg-black bg-opacity-50 transition-opacity"
              onClick={closeMobileMenu}
            ></div>
            <div className={`absolute top-0 right-0 bottom-0 w-1/2 max-w-sm ${darkMode ? 'bg-slate-800' : 'bg-white'} shadow-xl transform transition-transform duration-300 ease-in-out translate-x-0`}>
              <div className="flex flex-col h-full">
                <div className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-slate-700">
                  <h2 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Menu</h2>
                  <button
                    onClick={closeMobileMenu}
                    className={`p-2 rounded-lg transition-colors duration-200 ${
                      darkMode
                        ? 'text-gray-300 hover:bg-slate-700'
                        : 'text-gray-700 hover:bg-gray-200'
                    }`}
                    aria-label="Close menu"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                <div className="flex-1 flex flex-col p-4 space-y-4">
                  <button
                    onClick={() => {
                      router.push('/dashboard/tasks/create');
                      closeMobileMenu();
                    }}
                    className="px-4 py-3 rounded-lg text-left transition-colors duration-200 font-medium bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700"
                  >
                    Create Task
                  </button>

                  <button
                    onClick={() => {
                      router.push('/dashboard/tasks');
                      closeMobileMenu();
                    }}
                    className="px-4 py-3 rounded-lg text-left transition-colors duration-200 font-medium bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700"
                  >
                    View All Tasks
                  </button>

                  <button
                    onClick={() => {
                      router.push('/dashboard');
                      closeMobileMenu();
                    }}
                    className={`px-4 py-3 rounded-lg text-left transition-colors duration-200 font-medium ${
                      pathname === '/dashboard' && !pathname.includes('/tasks')
                        ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
                        : `${darkMode ? 'bg-slate-700 text-white hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-600' : 'bg-gray-100 text-gray-900 hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-600 hover:text-indigo-600'}`
                    }`}
                  >
                    Dashboard
                  </button>
                </div>

                <div className="p-4 border-t border-gray-200 dark:border-slate-700">
                  <button
                    onClick={async () => {
                      try {
                        await apiClient.logout();
                      } catch (error) {
                        console.error('Logout error:', error);
                      } finally {
                        authUtils.logout();
                        window.location.href = '/';
                      }
                    }}
                    className="w-full px-4 py-2 rounded-lg text-center transition-colors duration-200 font-medium bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        <main>
          <div className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              {children}
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}