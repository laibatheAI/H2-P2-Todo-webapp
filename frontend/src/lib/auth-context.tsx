'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authUtils } from './auth';
import { User } from '../../../shared/types/api-contracts';
import {apiClient} from './api-client';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (credentials: { email: string; password: string }) => Promise<{ user: User | null; error: string | null }>;
  register: (userData: { email: string; password: string; name: string }) => Promise<{ user: User | null; error: string | null }>;
  logout: () => void;
  checkAuthStatus: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check authentication status on initial load
    checkAuthStatus();

    // Ensure the API client has the token if it exists in localStorage
    const token = authUtils.getToken();
    if (token) {
      apiClient.setToken(token);
    }
  }, []);

  const checkAuthStatus = () => {
    setLoading(true);
    try {
      if (authUtils.isAuthenticated()) {
        const userData = authUtils.getUser();
        if (userData) {
          setUser(userData);
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } else {
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials: { email: string; password: string }) => {
    const result = await authUtils.login(credentials);
    if (result.user) {
      setUser(result.user);
      setIsAuthenticated(true);
    }
    return result;
  };

  const register = async (userData: { email: string; password: string; name: string }) => {
    const result = await authUtils.register(userData);
    if (result.user) {
      setUser(result.user);
      setIsAuthenticated(true);
    }
    return result;
  };

  const logout = () => {
    authUtils.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}