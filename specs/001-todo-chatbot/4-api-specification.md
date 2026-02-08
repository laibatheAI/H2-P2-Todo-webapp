# API Specification: Todo AI Chatbot

## Overview

The Todo AI Chatbot exposes a single stateless endpoint that handles all conversational interactions. The API follows REST principles and maintains no server-side state between requests.

## Endpoint: POST /api/{user_id}/chat

### Path Parameters
- `user_id` (string, required): The unique identifier of the authenticated user

### Request Schema

```json
{
  "message": {
    "role": "user",
    "content": "Natural language message from the user"
  },
  "metadata": {
    "timestamp": "ISO 8601 timestamp of the message",
    "client_info": {
      "platform": "Client platform (web, mobile, etc.)",
      "version": "Client version"
    }
  }
}
```

### Response Schema

```json
{
  "conversation_id": "Unique identifier for the conversation",
  "response": {
    "role": "assistant",
    "content": "Natural language response to the user",
    "tool_calls": [
      {
        "id": "Unique identifier for the tool call",
        "type": "function",
        "function": {
          "name": "Name of the MCP tool called",
          "arguments": "JSON string of tool arguments"
        }
      }
    ],
    "tool_results": [
      {
        "tool_call_id": "ID of the corresponding tool call",
        "result": "Result from the MCP tool execution"
      }
    ]
  },
  "timestamp": "ISO 8601 timestamp of the response",
  "metadata": {
    "processing_time_ms": "Time taken to process the request in milliseconds"
  }
}
```

### HTTP Status Codes
- `200 OK`: Request processed successfully
- `400 Bad Request`: Invalid request format or missing required fields
- `401 Unauthorized`: Authentication token missing or invalid
- `403 Forbidden`: User does not have access to the specified user_id
- `404 Not Found`: User or conversation not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side processing error

### Headers
- `Authorization`: Bearer token containing the user's JWT
- `Content-Type`: application/json
- `Accept`: application/json

### Rate Limiting
- Per-user rate limits: 100 requests per minute
- Burst allowance: Up to 20 requests in a 1-second window

### Conversation Lifecycle Rules

1. **Conversation Initiation**:
   - If no conversation exists for the user, a new conversation is created
   - First message establishes the conversation context

2. **Message Persistence**:
   - Each user message is persisted to the database upon receipt
   - Each assistant response is persisted to the database after generation

3. **Context Loading**:
   - Previous conversation history is loaded from database for each request
   - Only the most recent 50 messages are loaded to optimize performance

4. **Conversation Continuity**:
   - Conversations remain accessible across server restarts
   - Conversation state is fully restored from database

### Stateless Request Handling Guarantees

1. **No In-Memory State**:
   - Server does not store conversation state in memory
   - Each request contains all necessary context from database

2. **Idempotent Operations**:
   - Same request with identical parameters produces consistent results
   - Safe retries without side effects

3. **Complete Request Context**:
   - Each request loads full conversation history from database
   - Agent operates with complete context regardless of server state

4. **User Isolation**:
   - Requests for different users are completely isolated
   - No cross-contamination of user data or conversation context

### Authentication and Authorization

1. **Token Validation**:
   - JWT token is validated on each request
   - Token must contain valid user_id matching the path parameter

2. **User Verification**:
   - User account existence verified against database
   - Active account status confirmed

3. **Scope Validation**:
   - Requests only access data belonging to the authenticated user
   - Cross-user data access prevented

### Error Handling

1. **Client Errors (4xx)**:
   - Invalid request format returns 400 with detailed error message
   - Authentication failures return 401
   - Authorization failures return 403

2. **Server Errors (5xx)**:
   - MCP tool failures logged and return 500 with generic message
   - Database connectivity issues return 500
   - Agent processing errors return 500 with safe error message

### Logging and Monitoring

1. **Request Logging**:
   - All requests logged with anonymized content
   - Processing times recorded for performance monitoring

2. **Error Logging**:
   - All errors logged with correlation IDs
   - Sensitive data excluded from logs

3. **Audit Trail**:
   - All user actions recorded for compliance
   - Tool executions tracked for debugging