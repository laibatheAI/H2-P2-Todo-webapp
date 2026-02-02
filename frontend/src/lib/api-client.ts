import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  User,
  UserRegistrationRequest,
  UserRegistrationResponse,
  UserLoginRequest,
  UserLoginResponse,
  Task,
  TaskCreateRequest,
  TaskUpdateRequest,
  TaskToggleResponse
} from '../../../shared/types/api-contracts';

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  
  // constructor() {
  //   this.client = axios.create({
  //     baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  //     timeout: 15000, // Increased timeout to 15 seconds
  //   });

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
      timeout: 15000, // Increased timeout to 15 seconds
    });

    // Initialize token from localStorage if available
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('todo_app_token');
      if (storedToken) {
        this.token = storedToken;
      }
    }

    // Add request interceptor to include token in headers
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle token expiration
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token might be expired, clear it
          this.clearToken();
          // Don't redirect here - let the calling component handle unauthorized errors
          // This allows the auth context to properly detect and handle auth status
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string): void {
    this.token = token;
  }

  clearToken(): void {
    this.token = null;
  }

  // Authentication endpoints
  async register(userData: UserRegistrationRequest): Promise<AxiosResponse<UserRegistrationResponse>> {
    return this.client.post('/api/auth/register', userData);
  }

  async login(credentials: UserLoginRequest): Promise<AxiosResponse<UserLoginResponse>> {
    return this.client.post('/api/auth/login', credentials);
  }

  async logout(): Promise<AxiosResponse> {
    return this.client.post('/api/auth/logout');
  }

  // User endpoints
  async getCurrentUser(): Promise<AxiosResponse<User>> {
    return this.client.get('/api/auth/me');
  }

  // Task endpoints
  async getTasks(): Promise<AxiosResponse<Task[]>> {
    return this.client.get('/api/tasks');
  }

  async createTask(taskData: TaskCreateRequest): Promise<AxiosResponse<Task>> {
    return this.client.post('/api/tasks', taskData);
  }

  async getTask(taskId: string): Promise<AxiosResponse<Task>> {
    return this.client.get(`/api/tasks/${taskId}`);
  }

  async updateTask(taskId: string, taskData: TaskUpdateRequest): Promise<AxiosResponse<Task>> {
    return this.client.put(`/api/tasks/${taskId}`, taskData);
  }

  async deleteTask(taskId: string): Promise<AxiosResponse<void>> {
    return this.client.delete(`/api/tasks/${taskId}`);
  }

  async toggleTask(taskId: string): Promise<AxiosResponse<TaskToggleResponse>> {
    return this.client.patch(`/api/tasks/${taskId}/toggle`);
  }
}

// Export a singleton instance
export const apiClient = new ApiClient();

// Export the class for potential multiple instances if needed
export default ApiClient;