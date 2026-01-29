// Shared TypeScript types for API contracts between frontend and backend

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  created_at: string;
  updated_at: string;
}

export interface UserRegistrationRequest {
  email: string;
  password: string;
  name: string;
}

export interface UserRegistrationResponse {
  id: string;
  email: string;
  name: string;
  created_at: string;
  access_token: string;
  user: User;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface UserLoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface TaskToggleResponse {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}