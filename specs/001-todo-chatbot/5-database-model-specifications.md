# Database Model Specifications: Todo AI Chatbot

## Overview

This document defines the database models for the Todo AI Chatbot, designed using SQLModel with Neon Serverless PostgreSQL. All models implement user-level data isolation and proper indexing for performance.

## Model: Task

### Fields and Types
- `id` (UUID, primary key, default: gen_random_uuid()): Unique identifier for the task
- `user_id` (UUID, foreign key): Reference to the user who owns the task
- `title` (VARCHAR(255), not null): Title of the task
- `description` (TEXT): Detailed description of the task
- `due_date` (TIMESTAMP): Due date and time for the task
- `priority` (VARCHAR(20), default: 'medium'): Priority level ('low', 'medium', 'high')
- `category` (VARCHAR(100)): Category for organizing tasks
- `completed` (BOOLEAN, default: false): Completion status of the task
- `completed_at` (TIMESTAMP): Timestamp when task was marked as completed
- `created_at` (TIMESTAMP, default: CURRENT_TIMESTAMP): Creation timestamp
- `updated_at` (TIMESTAMP, default: CURRENT_TIMESTAMP): Last update timestamp

### Relationships
- Belongs to one User (many-to-one relationship)
- Indexed on `user_id` for efficient user-scoped queries

### User-Level Data Isolation
- All queries must filter by `user_id` to ensure data isolation
- Foreign key constraint ensures referential integrity
- Row-level security policies prevent cross-user data access

### Indexing and Constraints
- Primary key index on `id`
- Composite index on `(user_id, created_at)` for efficient chronological queries
- Index on `(user_id, completed)` for status-based filtering
- Index on `(user_id, due_date)` for deadline-based queries
- Index on `(user_id, priority)` for priority-based queries
- Check constraint on `priority` field to ensure valid values
- Not-null constraint on `user_id` and `title`

## Model: Conversation

### Fields and Types
- `id` (UUID, primary key, default: gen_random_uuid()): Unique identifier for the conversation
- `user_id` (UUID, foreign key): Reference to the user who owns the conversation
- `title` (VARCHAR(255)): Auto-generated title based on conversation topic
- `created_at` (TIMESTAMP, default: CURRENT_TIMESTAMP): Creation timestamp
- `updated_at` (TIMESTAMP, default: CURRENT_TIMESTAMP): Last activity timestamp
- `last_accessed_at` (TIMESTAMP, default: CURRENT_TIMESTAMP): Last access timestamp

### Relationships
- Belongs to one User (many-to-one relationship)
- Has many Messages (one-to-many relationship)
- Indexed on `user_id` for efficient user-scoped queries

### User-Level Data Isolation
- All queries must filter by `user_id` to ensure data isolation
- Foreign key constraint ensures referential integrity
- Row-level security policies prevent cross-user data access

### Indexing and Constraints
- Primary key index on `id`
- Index on `user_id` for efficient user-scoped queries
- Index on `user_id` and `updated_at` for chronological conversation retrieval
- Index on `user_id` and `last_accessed_at` for recency-based queries

## Model: Message

### Fields and Types
- `id` (UUID, primary key, default: gen_random_uuid()): Unique identifier for the message
- `conversation_id` (UUID, foreign key): Reference to the conversation this message belongs to
- `user_id` (UUID, foreign key): Reference to the user who owns this conversation/message
- `role` (VARCHAR(20), not null): Role of the message sender ('user', 'assistant')
- `content` (TEXT, not null): Content of the message
- `tool_calls` (JSONB): Array of tool calls made in this message
- `tool_results` (JSONB): Results from tool executions
- `created_at` (TIMESTAMP, default: CURRENT_TIMESTAMP): Creation timestamp

### Relationships
- Belongs to one Conversation (many-to-one relationship)
- Belongs to User through conversation (many-to-one relationship)
- Indexed on `conversation_id` for efficient conversation-scoped queries
- Indexed on `user_id` for user-scoped queries

### User-Level Data Isolation
- All queries must filter by `user_id` to ensure data isolation
- Foreign key constraint ensures referential integrity
- Additional `user_id` column provides redundant safety against conversation ID spoofing
- Row-level security policies prevent cross-user data access

### Indexing and Constraints
- Primary key index on `id`
- Index on `conversation_id` for conversation-scoped queries
- Composite index on `(conversation_id, created_at)` for chronological message retrieval
- Index on `user_id` for user-scoped queries
- Index on `role` for role-based filtering
- Not-null constraint on `conversation_id`, `user_id`, `role`, and `content`
- Foreign key constraint linking `conversation_id` to `conversations.id`
- Foreign key constraint linking `user_id` to `users.id`

## Database Schema Considerations

### UUID Primary Keys
- All primary keys use UUIDs for global uniqueness
- Prevents conflicts in distributed systems
- Enables secure referencing without exposing sequential IDs

### Timestamp Management
- `created_at` fields are set once at record creation
- `updated_at` fields are automatically updated on any modification
- Uses database triggers for consistent timestamp management

### JSONB for Flexible Data
- `tool_calls` and `tool_results` use JSONB for flexible tool execution data
- Enables efficient querying of JSON content
- Supports indexing on JSON fields when needed

### Performance Optimization
- Indexes strategically placed for common query patterns
- Composite indexes for multi-field queries
- Appropriate data types for efficient storage and retrieval

### Data Integrity
- Foreign key constraints ensure referential integrity
- Check constraints enforce business rules at database level
- Not-null constraints prevent incomplete records