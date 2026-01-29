# Todo Full-Stack Web Application

A secure, multi-user Todo web application with Next.js frontend and FastAPI backend. The system provides user registration/authentication with JWT-based security, task CRUD functionality with user isolation, and persistent storage using Neon PostgreSQL.

## Features

- User registration and authentication with JWT tokens
- Secure task management with user isolation
- Responsive web interface
- RESTful API with proper authorization
- Concurrent session support per user

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: Python 3.11+, FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT-based with configurable expiration

## Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL (or Neon PostgreSQL account)
- pnpm or npm for frontend package management
- uv for Python dependency management (or pip)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-fullstack-app
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install  # or npm install
```

### 4. Environment Configuration

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

### 5. Database Setup

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

## Running the Application

### 1. Start Backend Server

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn src.main:app --reload --port 8000
```

### 2. Start Frontend Server

```bash
cd frontend
pnpm dev  # or npm run dev
```

The application will be accessible at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Tasks
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion status

## Security Features

- JWT-based authentication with 1-hour access tokens and 7-day refresh tokens
- User data isolation - users can only access their own tasks
- Password hashing with bcrypt
- Input validation and sanitization

## Development

The application follows a monorepo structure with clear separation between frontend and backend components. All changes should be made following the established patterns in the codebase.

## License

[Specify license type here]