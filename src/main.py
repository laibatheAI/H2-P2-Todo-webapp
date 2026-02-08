from fastapi import FastAPI, Depends, Path, HTTPException, status
from typing import Dict, Any
import time
import uuid
from datetime import datetime

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

# Include routes here once they are created
try:
    # Import specific functions to adapt the backend router to the required path structure
    from backend.api.v1.endpoints.chat import chat_endpoint as backend_chat_endpoint, chat_health_check
    from backend.schemas.chat import ChatRequest

    # Create the exact endpoint as specified: POST /api/{user_id}/chat
    @app.post("/api/{user_id}/chat", tags=["chat"])
    async def chat_endpoint_wrapper(
        user_id: str = Path(..., description="The unique identifier of the authenticated user"),
        chat_request: ChatRequest = None
    ):
        # Forward to the backend implementation, adapting the path parameter
        return await backend_chat_endpoint(user_id, chat_request)

    # Also expose health check at the expected path
    @app.get("/api/{user_id}/chat/health", tags=["chat"])
    async def health_check_endpoint(
        user_id: str = Path(..., description="The unique identifier of the user (for path validation)")
    ):
        return await chat_health_check(user_id)

except ImportError as e:
    print(f"Chat router not available yet: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
