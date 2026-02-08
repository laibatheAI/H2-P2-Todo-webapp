# Stateless Conversation Flow: Todo AI Chatbot

## Overview

This document outlines the step-by-step request lifecycle for the Todo AI Chatbot, ensuring complete statelessness while maintaining conversation continuity through database persistence.

## Request Lifecycle

### Step 1: Receive Request
- API endpoint receives POST request at `/api/{user_id}/chat`
- Validates request headers and authorization token
- Verifies JWT contains valid user_id matching path parameter
- Ensures request body conforms to expected schema

### Step 2: Load Conversation History from Database
- Query database for conversation associated with user_id
- If no conversation exists, create new conversation record
- Retrieve last N messages (default 50) from the conversation's message history
- Order messages chronologically (oldest to newest)
- Construct conversation context for the AI agent

### Step 3: Persist User Message
- Create new Message record in database with role='user'
- Link message to conversation_id
- Store original user content and metadata
- Update conversation's `updated_at` and `last_accessed_at` timestamps
- Ensure message is persisted before proceeding

### Step 4: Run Agent with MCP Tools
- Initialize AI agent with complete conversation history
- Process user message through intent classification
- Select appropriate MCP tools based on identified intent
- Execute MCP tools with validated parameters
- Collect tool call results and errors

### Step 5: Persist Assistant Response
- Create new Message record in database with role='assistant'
- Store assistant response content and tool execution results
- Link message to same conversation_id
- Update conversation's `updated_at` and `last_accessed_at` timestamps
- Ensure response is persisted before returning to client

### Step 6: Return Response to Client
- Format response according to API specification
- Include conversation_id for continuity
- Include tool calls and results if applicable
- Add metadata including processing time
- Return HTTP 200 with response payload

## Statelessness Guarantees

### No In-Memory State
- Server maintains no conversation state between requests
- Each request rebuilds context from database
- Multiple server instances operate identically
- Server restarts do not affect conversation continuity

### Complete Context Reconstruction
- Full conversation history loaded from database for each request
- Agent operates with complete context regardless of server state
- No reliance on cached or stored conversation state
- Consistent behavior across server instances

### Idempotent Operations
- Same input produces same output regardless of server state
- Safe to retry requests without side effects
- Predictable behavior for client applications
- Resilient to network interruptions

## Error Handling During Flow

### Database Connection Failures
- If unable to load conversation history, return 500 error
- If unable to persist user message, return 500 error
- If unable to persist assistant response, return 500 error but attempt to complete operation

### Authentication Failures
- If JWT validation fails, return 401 Unauthorized immediately
- No database operations performed if authentication fails
- No information leaked about user existence

### MCP Tool Failures
- Failed tool executions are captured and included in response
- Agent continues operation despite individual tool failures
- Error messages formatted for user consumption
- Tool execution errors logged for system monitoring

## Performance Considerations

### Conversation History Optimization
- Limit loaded messages to reasonable number (default 50)
- Use database indexing for efficient history retrieval
- Implement pagination for very long conversations
- Cache frequently accessed conversation metadata

### Database Transaction Management
- Use transactions for atomic operations (persisting messages)
- Ensure data consistency during concurrent operations
- Optimize transaction scope to minimize lock duration
- Handle transaction conflicts gracefully

### Resource Management
- Close database connections properly after each request
- Manage memory usage during conversation history loading
- Implement connection pooling for database efficiency
- Monitor resource usage during peak loads

## Security Measures

### User Data Isolation
- Verify user_id in JWT matches database records
- Filter all queries by user_id to prevent data leakage
- Validate conversation ownership before access
- Implement row-level security where possible

### Input Validation
- Validate user message content before processing
- Sanitize inputs before database storage
- Validate tool parameters before execution
- Protect against injection attacks

### Audit Trail
- Log all conversation operations for compliance
- Track user authentication and authorization
- Record tool execution for debugging
- Maintain secure access logs