'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function HomePage() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    // Check for saved dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(savedDarkMode);

    // Apply dark mode class to document if needed
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

  return (
    <div className={`min-h-screen flex flex-col ${darkMode ? 'bg-gradient-to-br from-gray-900 via-indigo-900 to-gray-900' : 'bg-gradient-to-br from-emerald-teal-50 to-emerald-teal-100'}`}>
      {/* Navigation */}
      <nav className={`px-4 sm:px-6 lg:px-8 py-6 ${darkMode ? 'bg-gray-800/50' : 'bg-white'} backdrop-blur-sm border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <h1 className={`text-2xl font-bold ${darkMode ? 'bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent' : 'bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent'}`}>
              TaskNest
            </h1>
          </div>

          <div className="flex items-center space-x-4">
            {/* Dark mode toggle - visible on all screen sizes */}
            <button
              onClick={toggleDarkMode}
              className={`p-2 rounded-full transition-colors duration-200 ${
                darkMode ? 'text-yellow-400 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-200'
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

            <div className="hidden sm:flex items-center space-x-4">
              <Link
                href="/auth/login"
                className={`${darkMode ? 'text-gray-300 hover:text-white' : 'text-indigo-600 hover:text-indigo-700'} transition-colors duration-200 font-medium`}
              >
                Sign In
              </Link>
              <Link
                href="/auth/register"
                className={`px-4 py-2 rounded-lg font-semibold border transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-opacity-50 ${
                  darkMode
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-indigo-500 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/30 focus:ring-indigo-500'
                    : 'bg-white hover:bg-gray-100 text-indigo-600 border-indigo-500 focus:ring-indigo-500'
                }`}
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-grow flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl w-full text-center">
          <h1 className="text-3xl md:text-7xl font-bold mb-3 mt-6 text-center">
            <span className={`bg-gradient-to-r ${darkMode ? 'from-indigo-400 via-purple-400 to-pink-400' : 'from-indigo-600 via-purple-500 to-indigo-400'} bg-clip-text text-transparent`}>
              Organize Your Life
            </span>
          </h1>
          <p className={`text-1px md:text-2xl ${darkMode ? 'text-gray-300' : 'text-gray-700'} mb-10 max-w-2xl mx-auto text-center`}>
            𝑻𝒂𝒔𝒌𝑵𝒆𝒔𝒕 𝒉𝒆𝒍𝒑𝒔 𝒚𝒐𝒖 𝒎𝒂𝒏𝒂𝒈𝒆 𝒚𝒐𝒖𝒓 𝒕𝒂𝒔𝒌𝒔 𝒆𝒇𝒇𝒊𝒄𝒊𝒆𝒏𝒕𝒍𝒚 𝒘𝒊𝒕𝒉 𝒂 𝒃𝒆𝒂𝒖𝒕𝒊𝒇𝒖𝒍, 𝒊𝒏𝒕𝒖𝒊𝒕𝒊𝒗𝒆 𝒊𝒏𝒕𝒆𝒓𝒇𝒂𝒄𝒆 𝒅𝒆𝒔𝒊𝒈𝒏𝒆𝒅 𝒇𝒐𝒓 𝒑𝒓𝒐𝒅𝒖𝒄𝒕𝒊𝒗𝒊𝒕𝒚.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              href="/auth/register"
              className={`px-7 py-4 text-lg font-bold rounded-xl font-semibold border transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-opacity-50 ${
                darkMode
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-indigo-500 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/30 focus:ring-indigo-500'
                  : 'bg-white hover:bg-gray-100 text-indigo-600 border-indigo-500 focus:ring-indigo-500 shadow-indigo-500/25'
              }`}
            >
              Get Started
            </Link>
            <Link
              href="/auth/login"
              className={`px-12 py-4 text-lg font-bold rounded-xl font-semibold border transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-opacity-50 ${
                darkMode
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-indigo-500 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/30 focus:ring-indigo-500'
                  : 'bg-white hover:bg-gray-100 text-indigo-600 border-indigo-500 focus:ring-indigo-500 shadow-indigo-500/25'
              }`}
            >
              Sign In
            </Link>
          </div>

          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className={`${darkMode ? 'bg-gray-800/30' : 'bg-white/30'} backdrop-blur-lg rounded-2xl p-6 border ${darkMode ? 'border-teal-700' : 'border-indigo-600'}`}>
              <div className={`${darkMode ? 'text-indigo-400' : 'text-indigo-500'} text-3xl mb-3`}>📝</div>
              <h3 className={`text-xl font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-800'} mb-2`}>Easy Task Management</h3>
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Intuitive interface to create, organize, and track your tasks effortlessly.</p>
            </div>

            <div className={`${darkMode ? 'bg-gray-800/30' : 'bg-white/30'} backdrop-blur-lg rounded-2xl p-6 border ${darkMode ? 'border-teal-700' : 'border-indigo-600'}`}>
              <div className={`${darkMode ? 'text-indigo-400' : 'text-indigo-500'} text-3xl mb-3`}>🔒</div>
              <h3 className={`text-xl font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-800'} mb-2`}>Secure & Private</h3>
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Your data is encrypted and stored securely with industry-standard practices.</p>
            </div>

            <div className={`${darkMode ? 'bg-gray-800/30' : 'bg-white/30'} backdrop-blur-lg rounded-2xl p-6 border ${darkMode ? 'border-teal-700' : 'border-indigo-600'}`}>
              <div className={`${darkMode ? 'text-indigo-400' : 'text-indigo-500'} text-3xl mb-3`}>⚡</div>
              <h3 className={`text-xl font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-800'} mb-2`}>Cross Platform</h3>
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Access your tasks anywhere, anytime across all your devices.</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className={`py-8 px-4 sm:px-6 lg:px-8 border-t ${darkMode ? 'border-gray-800' : 'border-indigo-200'}`}>
        <div className="max-w-4xl mx-auto text-center text-gray-400">
          <p>© {new Date().getFullYear()} TaskNest. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}