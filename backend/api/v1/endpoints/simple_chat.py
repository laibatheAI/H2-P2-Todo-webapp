"""
Simple chat API endpoint for the Todo AI Chatbot application.
This is a minimal implementation to ensure the endpoint is registered.
"""
from fastapi import APIRouter, Path, HTTPException, status, Body
from typing import Dict, Any
import time
import uuid
from datetime import datetime

from backend.schemas.chat import ChatRequest, ChatResponse, ErrorResponse, AssistantMessage, ResponseMetadata


router = APIRouter()


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str = Path(..., description="The unique identifier of the authenticated user"),
    chat_request: ChatRequest = Body(...)
) -> ChatResponse:
    """
    Simple chat endpoint that returns a basic response.
    This is a minimal implementation to verify the endpoint is working.
    """
    start_time = time.time()

    try:
        # Generate a conversation ID for this interaction
        conversation_id = str(uuid.uuid4())

        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Create a simple response
        assistant_message = AssistantMessage(
            role="assistant",
            content="Hello! This is a test response from the chatbot. Your message was received.",
            tool_calls=[],
            tool_results=[]
        )

        response = ChatResponse(
            conversation_id=conversation_id,
            response=assistant_message,
            timestamp=datetime.utcnow(),
            metadata=ResponseMetadata(processing_time_ms=processing_time_ms)
        )

        return response

    except Exception as e:
        # Calculate processing time even for errors
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Log the error (in a real implementation)
        print(f"Error in chat endpoint: {str(e)}")

        # Return error response
        error_response = ErrorResponse(
            success=False,
            error=str(e),
            message="An error occurred while processing your request. Please try again.",
            timestamp=datetime.utcnow()
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.dict()
        )