import logging
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(backend_dir))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
from .database.init_db import create_db_and_tables
from .utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    logger.info("Starting up Todo API application")
    create_db_and_tables()
    logger.info("Database tables initialized successfully")
    yield
    # Cleanup on shutdown if needed
    logger.info("Shutting down Todo API application")

# Custom middleware to handle proxy headers from HuggingFace
class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check for forwarded protocol headers from HuggingFace proxy
        forwarded_proto = request.headers.get('x-forwarded-proto')

        # If the request came through HTTPS originally but FastAPI sees it as HTTP,
        # we need to handle this appropriately for redirects and URL generation
        if forwarded_proto and forwarded_proto.lower() == 'https':
            # Update the request's scope to reflect the original HTTPS protocol
            request.scope['scheme'] = 'https'

        response = await call_next(request)
        return response

# Create FastAPI app with security-focused settings
app = FastAPI(
    title="Todo API",
    description="Secure Todo application API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Add custom ProxyHeadersMiddleware to handle X-Forwarded-* headers from HuggingFace proxy
app.add_middleware(ProxyHeadersMiddleware)

# Add TrustedHostMiddleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.hf.space", "localhost", "127.0.0.1", "*.vercel.app"]
)

# Add CORS middleware with HTTPS origins only for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add routes
# Import the chat router using a direct path approach
import os
import sys

# Add the parent directory (backend) to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/src
parent_dir = os.path.dirname(current_dir)  # backend
original_path = sys.path[:]
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Import the chat module directly using the absolute path approach
    import importlib.util
    chat_module_path = os.path.join(parent_dir, 'api', 'v1', 'endpoints', 'chat.py')
    spec = importlib.util.spec_from_file_location("chat", chat_module_path)
    chat_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(chat_module)
    
    # Get the router from the loaded module
    chat_router = chat_module.router
    app.include_router(chat_router)  # No prefix since path is defined in the endpoint
    print("Chat router loaded successfully")
except Exception as e:
    print(f"Chat router not found: {e}")
finally:
    # Restore the original path
    sys.path[:] = original_path

app.include_router(auth_router)
app.include_router(tasks_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Add exception handlers for better error management
@app.exception_handler(Exception)
async def internal_exception_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}", exc_info=True)
    return {"message": "Internal server error occurred"}