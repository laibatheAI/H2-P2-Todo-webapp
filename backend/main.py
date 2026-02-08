from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Todo AI Chatbot API",
    description="Stateless Todo AI Chatbot with MCP tools integration",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"Hello": "Todo AI Chatbot"}

# Include routes
from backend.api.v1.endpoints import chat
app.include_router(chat.router, tags=["chat"])  # No prefix since path is defined in the endpoint

# Import and register other API routes if they exist
try:
    from backend.src.api.auth import router as auth_router
    app.include_router(auth_router, prefix="/api", tags=["auth"])
except ImportError:
    pass

try:
    from backend.src.api.tasks import router as tasks_router
    app.include_router(tasks_router, prefix="/api", tags=["tasks"])
except ImportError:
    pass