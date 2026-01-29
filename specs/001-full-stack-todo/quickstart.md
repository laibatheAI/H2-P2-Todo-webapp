# Quickstart Guide: Todo Full-Stack Web Application

**Feature**: 001-full-stack-todo
**Date**: 2026-01-06

## Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL (or Neon PostgreSQL account)
- pnpm or npm for frontend package management
- uv for Python dependency management (or pip)

## Environment Setup

### 1. Clone and Initialize Repository

```bash
# Create the monorepo structure
mkdir todo-fullstack-app
cd todo-fullstack-app

# Initialize git repository
git init

# Create directory structure
mkdir -p backend/src/{models,services,api,database}
mkdir -p frontend/src/{app,components,lib,types}
mkdir -p shared/types
```

### 2. Backend Setup (Python/FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create requirements.txt
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
sqlmodel==0.0.16
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
better-exceptions==0.3.3
python-multipart==0.0.9
asyncpg==0.29.0
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
EOF

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup (Next.js)

```bash
cd ../frontend

# Initialize Next.js project
pnpm create next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Install additional dependencies
pnpm add @types/node better-auth react-icons
pnpm add -D @types/react @types/react-dom
```

### 4. Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
BETTER_AUTH_URL=http://localhost:3000
DATABASE_SSL_REQUIRED=false
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Development Workflow

### 1. Start Backend Server

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn src.main:app --reload --port 8000
```

### 2. Start Frontend Server

```bash
cd frontend
pnpm dev
```

### 3. Database Setup

```bash
# With backend virtual environment activated
cd backend
python -c "
from sqlmodel import SQLModel, create_engine
from src.database.database import DATABASE_URL
engine = create_engine(DATABASE_URL)
from src.models.user import User
from src.models.task import Task
SQLModel.metadata.create_all(engine)
print('Database tables created successfully!')
"
```

## API Contract Overview

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Task Endpoints
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion status

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
pnpm test
```