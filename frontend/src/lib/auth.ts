import { apiClient } from './api-client';
import { User, UserRegistrationRequest, UserLoginRequest } from '../../../shared/types/api-contracts';

// Key for storing JWT token in localStorage
const TOKEN_KEY = 'todo_app_token';
const USER_KEY = 'todo_app_user';

// Auth utility functions
export const authUtils = {
  // Store token in localStorage
  setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
    // Update the API client with the new token
    apiClient.setToken(token);
  },

  // Get token from localStorage
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  },

  // Remove token from localStorage
  removeToken(): void {
    localStorage.removeItem(TOKEN_KEY);
    // Clear token from API client
    apiClient.clearToken();
  },

  // Store user in localStorage
  setUser(user: User): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  // Get user from localStorage
  getUser(): User | null {
    const userStr = localStorage.getItem(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  },

  // Remove user from localStorage
  removeUser(): void {
    localStorage.removeItem(USER_KEY);
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!this.getToken();
  },

  // Register a new user
  async register(userData: UserRegistrationRequest): Promise<{ user: User | null, error: string | null }> {
    try {
      const response = await apiClient.register(userData);
      const { access_token, user } = response.data;

      // Store the token and user
      this.setToken(access_token);
      this.setUser(user);

      return { user, error: null };
      
    } catch (error: any) {
      let errorMessage = 'Registration failed';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }
      return { user: null, error: errorMessage };
    }
  },

  // Login user
  async login(credentials: UserLoginRequest): Promise<{ user: User | null, error: string | null }> {
    try {
      const response = await apiClient.login(credentials);
      const { access_token, user } = response.data;

      // Store the token and user
      this.setToken(access_token);
      this.setUser(user);

      return { user, error: null };
    } catch (error: any) {
      let errorMessage = 'Login failed';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }
      return { user: null, error: errorMessage };
    }
  },

  // Logout user
  logout(): void {
    this.removeToken();
    this.removeUser();
  },

  // Refresh token if expired
  async refreshToken(): Promise<boolean> {
    // In a real implementation, you would make a call to the backend to refresh the token
    // using the refresh token stored in localStorage or a secure cookie
    // For now, we'll return false indicating token refresh is not needed or failed
    return false;
  },

  // Method to check if token is about to expire
  isTokenExpiringSoon(): boolean {
    const token = this.getToken();
    if (!token) return true; // If no token, consider as expiring

    try {
      // Decode the token without verification to check expiry
      const payload = token.split('.')[1];
      const decodedPayload = JSON.parse(atob(payload));
      const currentTime = Math.floor(Date.now() / 1000);
      const timeUntilExpiry = decodedPayload.exp - currentTime;

      // Consider token as expiring if it expires in less than 5 minutes
      return timeUntilExpiry < 300;
    } catch (error) {
      return true; // If we can't decode the token, assume it's problematic
    }
  }
};