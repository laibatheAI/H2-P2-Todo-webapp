'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authUtils } from '../../../lib/auth';
import { UserLoginRequest } from '../../../../../shared/types/api-contracts';
import StatusCard from '@/components/StatusCard/StatusCard';

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<UserLoginRequest>({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [showSuccessNotification, setShowSuccessNotification] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Show success notification if user just registered
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('registered') === 'true') {
      setShowSuccessNotification(true);
      // Hide the notification after 5 seconds
      const timer = setTimeout(() => {
        setShowSuccessNotification(false);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
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

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    try {
      const result = await authUtils.login(formData);

      if (result.error) {
        setSubmitError(result.error);
      } else {
        // Show success notification and redirect after a delay
        setShowSuccessNotification(true);

        // Hide error if it was shown
        setSubmitError(null);

        // Wait a moment to show the success notification before redirecting
        setTimeout(() => {
          router.push('/dashboard');
        }, 1500);
      }
    } catch (error) {
      setSubmitError('An error occurred during login. Please try again.');
      console.error('Login error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-indigo-900 to-gray-900 p-4">
      {/* Background pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-indigo-900/20 via-transparent to-transparent"></div>

      {/* Notification overlay */}
      {showSuccessNotification && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
          <StatusCard
            status="success"
            message="Login successful! Welcome back to TaskNest." type={'success'}          />
        </div>
      )}

      <div className="relative max-w-md w-full">
        <div className="bg-black/30 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-700 p-10">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-2">
              TaskNest
            </h1>
            <p className="text-base text-gray-300">Organize your day. Own your time.</p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-5">
              <div>
                <label htmlFor="email-address" className="block text-sm font-medium text-gray-200 mb-2">
                  Email address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className={`w-full px-4 py-3.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200 backdrop-blur-sm ${
                    errors.email
                      ? 'border-rose-500 bg-red-900/20 text-rose-100'
                      : 'border-gray-600 bg-gray-800/50 text-gray-100'
                  }`}
                  placeholder="Enter your email"
                />
                {errors.email && (
                  <p className="mt-2 text-sm text-rose-400 font-medium">{errors.email}</p>
                )}
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-200 mb-2">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  className={`w-full px-4 py-3.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200 backdrop-blur-sm ${
                    errors.password
                      ? 'border-rose-500 bg-red-900/20 text-rose-100'
                      : 'border-gray-600 bg-gray-800/50 text-gray-100'
                  }`}
                  placeholder="Enter your password"
                />
                {errors.password && (
                  <p className="mt-2 text-sm text-rose-400 font-medium">{errors.password}</p>
                )}
              </div>
            </div>

            {submitError && (
              <div className="rounded-xl bg-red-900/30 p-4 border border-red-500/50">
                <p className="text-sm text-red-300 font-medium text-center">{submitError}</p>
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex justify-center py-3.5 px-4 border text-base font-semibold rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed bg-white hover:bg-gray-100 text-indigo-600 border-indigo-500 focus:ring-indigo-500 focus:ring-opacity-50 dark:bg-gradient-to-r dark:from-indigo-600 dark:to-purple-600 dark:text-white dark:border-indigo-500 dark:hover:from-indigo-700 dark:hover:to-purple-700 dark:focus:ring-indigo-500 dark:shadow-lg dark:shadow-indigo-500/30"
              >
                {isLoading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-indigo-600 dark:text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing In...
                  </span>
                ) : (
                  'Sign In'
                )}
              </button>
            </div>
          </form>

          <div className="mt-8 pt-6 border-t border-gray-700">
            <p className="text-center text-sm text-gray-400">
              Don't have an account?{' '}
              <Link href="/auth/register" className="font-semibold text-indigo-400 hover:text-indigo-300 transition-colors duration-200">
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}