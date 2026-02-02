import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Create FastAPI app with security-focused settings
app = FastAPI(
    title="Todo API",
    description="Secure Todo application API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Add security-related middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.hf.space", "localhost", "127.0.0.1"]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://h2-p2-todo-webapp.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add routes
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