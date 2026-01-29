# Todo API Documentation

## Base URL
`http://localhost:8000` (development) or your deployed URL

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2023-01-01T00:00:00",
  "access_token": "jwt-token-string",
  "refresh_token": "refresh-token-string",
  "token_type": "bearer"
}
```

#### POST /api/auth/login
Authenticate a user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "jwt-token-string",
  "refresh_token": "refresh-token-string",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "avatar": null,
    "created_at": "2023-01-01T00:00:00"
  }
}
```

#### POST /api/auth/logout
Logout user (currently just client-side)

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

#### GET /api/auth/me
Get current authenticated user

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar": null,
  "created_at": "2023-01-01T00:00:00"
}
```

### Tasks

#### GET /api/tasks
Get all tasks for the authenticated user

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": "uuid-string",
    "title": "Sample Task",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

#### POST /api/tasks
Create a new task

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description (optional)",
  "completed": false
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "New Task",
  "description": "Task description (optional)",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### GET /api/tasks/{task_id}
Get a specific task

**Parameters:**
- task_id: UUID of the task

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Task description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### PUT /api/tasks/{task_id}
Update a task

**Parameters:**
- task_id: UUID of the task

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### DELETE /api/tasks/{task_id}
Delete a task

**Parameters:**
- task_id: UUID of the task

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

#### PATCH /api/tasks/{task_id}/toggle
Toggle task completion status

**Parameters:**
- task_id: UUID of the task

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Task description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

## Error Responses

The API returns standard HTTP error codes:
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: Access denied to resource
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Rate Limiting
The API implements rate limiting to prevent abuse. Standard limits apply per IP address.

## Security Headers
All responses include security headers to prevent common attacks:
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection