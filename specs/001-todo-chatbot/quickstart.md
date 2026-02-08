# Todo AI Chatbot Quickstart Guide

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed (for frontend development)
- PostgreSQL database (Neon Serverless recommended)
- Better Auth configured in the codebase
- OpenAI API key
- MCP SDK installed

## Setup Instructions

### 1. Backend Setup
1. Install Python dependencies:
   ```bash
   pip install fastapi sqlmodel openai uvicorn python-jose[cryptography] python-multipart
   ```

2. Configure database connection in `backend/config.py`:
   ```python
   DATABASE_URL = "postgresql://username:password@host:port/dbname"
   ```

3. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export JWT_SECRET_KEY="your-jwt-secret"
   export MCP_SERVER_PORT=8001
   ```

### 2. Database Initialization
1. Run migrations to create required tables:
   ```bash
   alembic revision --autogenerate -m "Initial todo chatbot models"
   alembic upgrade head
   ```

2. Verify tables are created:
   - tasks table
   - conversations table
   - messages table

### 3. MCP Server Setup
1. Start the MCP server:
   ```bash
   python backend/mcp/server.py
   ```

2. Verify MCP tools are registered:
   - add_task
   - list_tasks
   - complete_task
   - delete_task
   - update_task

### 4. API Server Setup
1. Start the main FastAPI application:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

2. Verify the chat endpoint is accessible:
   - `POST /api/{user_id}/chat`

### 5. Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install @openai/chatkit
   ```

3. Configure environment variables:
   ```bash
   NEXT_PUBLIC_CHAT_API_URL="http://localhost:8000/api"
   NEXT_PUBLIC_MCP_SERVER_URL="http://localhost:8001"
   ```

## Running the Application

### Development Mode
1. Start MCP server: `python backend/mcp/server.py`
2. Start API server: `uvicorn backend.main:app --reload`
3. Start frontend: `npm run dev` (in frontend directory)

### Production Mode
1. Build frontend: `npm run build`
2. Start MCP server with gunicorn: `gunicorn backend.mcp.server:app`
3. Start API server with gunicorn: `gunicorn backend.main:app`

## Testing the Implementation

### Basic Conversation Test
1. Send a test message to the API:
   ```bash
   curl -X POST http://localhost:8000/api/user123/chat \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"message": {"role": "user", "content": "Add a task to buy groceries"}}'
   ```

2. Verify the response includes:
   - Conversation ID
   - Tool call to add_task
   - Proper JSON response format

### MCP Tool Test
1. Verify each MCP tool responds correctly:
   - `add_task`: Creates new task in database
   - `list_tasks`: Returns user's tasks
   - `complete_task`: Marks task as completed
   - `delete_task`: Removes task from database
   - `update_task`: Modifies task properties

### Authentication Test
1. Test with valid JWT: Should return successful response
2. Test with invalid JWT: Should return 401 Unauthorized
3. Test with wrong user_id: Should return 403 Forbidden

## Common Issues and Solutions

### Database Connection Issues
- Verify PostgreSQL is running and accessible
- Check database URL configuration
- Ensure proper credentials are provided

### Authentication Problems
- Confirm JWT is properly formatted
- Verify JWT secret key matches between auth and verification
- Check that user_id in path matches JWT user_id

### MCP Server Not Responding
- Verify MCP server is running on correct port
- Check that tools are properly registered
- Confirm agent can discover and call tools

## Environment Configuration

### Development Environment
```bash
# Backend
export DATABASE_URL="postgresql://localhost/todo_dev"
export JWT_SECRET_KEY="dev_secret_key_for_testing"
export OPENAI_API_KEY="sk-..."
export MCP_SERVER_PORT=8001
export ENVIRONMENT="development"

# Frontend
export NEXT_PUBLIC_CHAT_API_URL="http://localhost:8000/api"
export NEXT_PUBLIC_AUTH_ENABLED=true
```

### Production Environment
```bash
# Backend
export DATABASE_URL="postgresql://neon-serverless-url"
export JWT_SECRET_KEY="production_secret_key"
export OPENAI_API_KEY="sk-..."
export MCP_SERVER_PORT=80
export ENVIRONMENT="production"
export LOG_LEVEL="info"

# Frontend
export NEXT_PUBLIC_CHAT_API_URL="https://yourdomain.com/api"
export NEXT_PUBLIC_AUTH_ENABLED=true
```