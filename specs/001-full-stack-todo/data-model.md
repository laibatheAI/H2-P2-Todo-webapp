# Data Model: Todo Full-Stack Web Application

**Feature**: 001-full-stack-todo
**Date**: 2026-01-06

## Entity Definitions

### User Entity

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `email`: String (Required, unique, validated email format)
- `name`: String (Required, 2-100 characters)
- `avatar`: String (Optional, URL to avatar image)
- `created_at`: DateTime (Auto-generated timestamp)
- `updated_at`: DateTime (Auto-generated timestamp)

**Validation Rules**:
- Email must be a valid email format
- Name must be 2-100 characters
- Email must be unique across all users

**Relationships**:
- One-to-Many with Task entity (one user can have many tasks)

### Task Entity

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `title`: String (Required, 2-100 characters)
- `description`: String (Optional, up to 1000 characters)
- `completed`: Boolean (Default: false)
- `user_id`: UUID (Foreign Key, references User.id)
- `created_at`: DateTime (Auto-generated timestamp)
- `updated_at`: DateTime (Auto-generated timestamp)

**Validation Rules**:
- Title is required and must be 2-100 characters
- Description is optional and can be up to 1000 characters
- Completed defaults to false
- user_id must reference an existing user

**Relationships**:
- Many-to-One with User entity (many tasks belong to one user)

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    avatar TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## State Transitions

### Task State Transitions
- **Incomplete → Complete**: When user marks task as done
- **Complete → Incomplete**: When user unmarks task as done

## Indexes

- Index on `users.email` for efficient lookup during authentication
- Index on `tasks.user_id` for efficient user-specific task queries
- Index on `tasks.created_at` for chronological sorting