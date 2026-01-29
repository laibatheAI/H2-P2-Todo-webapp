'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authUtils } from '../../lib/auth';
import { apiClient } from '../../lib/api-client';

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

export default function ProtectedRoute({ children, redirectTo = '/auth/login' }: ProtectedRouteProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      if (authUtils.isAuthenticated()) {
        try {
          // Make a real API call to verify the token is still valid
          await apiClient.getCurrentUser();
          setIsAuthenticated(true);
        } catch (error) {
          // Token is not valid anymore, logout the user
          authUtils.logout();
          setIsAuthenticated(false);
        }
      } else {
        setIsAuthenticated(false);
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push(redirectTo);
    }
  }, [loading, isAuthenticated, redirectTo, router]);

  // Show loading indicator while checking auth status
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Don't render children until authentication status is determined
  // This prevents flashing of protected content before redirect
  if (!isAuthenticated) {
    return null; // Redirect will happen via useEffect
  }

  return <>{children}</>;
}