# Todo AI Chatbot – Phase III Implementation Plan

## Executive Summary

This document provides a detailed, phase-wise implementation plan for the Todo AI Chatbot, transforming the approved specifications into executable development phases. The implementation follows a stateless backend architecture with MCP tools integration and ChatKit frontend.

## Technical Context

### Repository Structure
- `backend/` - FastAPI backend with OpenAI Agents SDK, MCP integration, and JWT authentication
- `frontend/` - OpenAI ChatKit integration for user interaction
- `specs/001-todo-chatbot/` - Reference specifications (read-only)

### Technology Stack
- **Backend**: Python FastAPI
- **AI Logic**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **Frontend**: OpenAI ChatKit
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT-based (existing implementation)

### Architecture Principles
- Stateless server design with database-backed persistence
- User isolation through JWT-based scoping
- MCP tools for task management operations
- Event-driven conversation flow

## Constitution Check

### Applied Principles from Constitution
- **Security First**: All API endpoints require JWT authentication
- **User Data Isolation**: All queries scoped by authenticated user ID
- **Statelessness**: Server maintains no in-memory conversation state
- **Resilience**: Proper error handling and graceful degradation
- **Traceability**: Comprehensive logging for debugging and auditing

### Compliance Verification
- [x] All database operations include user ID scoping
- [x] Authentication required for all endpoints
- [x] No server-side session state maintained
- [x] Proper error handling for all operations
- [x] Secure token validation implemented

## Research & Unknown Resolution

### Phase 0: Research Findings

#### JWT Integration Strategy
**Decision**: Leverage existing Better Auth JWT implementation from codebase
**Rationale**: Consistent with project's authentication approach, reduces implementation risk
**Alternatives considered**: Custom JWT implementation, OAuth2 integration

#### MCP Server Architecture
**Decision**: Implement MCP server as FastAPI middleware component
**Rationale**: Integrates seamlessly with existing FastAPI stack, maintains statelessness
**Alternatives considered**: Standalone MCP server, external MCP service

#### OpenAI Agent Configuration
**Decision**: Initialize agent per request with MCP tools, ensuring complete statelessness
**Rationale**: Maintains conversation history from database while preserving statelessness
**Alternatives considered**: Persistent agent instances, shared agent pools

## Phase Breakdown

### Phase 1: Backend Foundation & Chat Module Setup

#### Objectives
- Set up FastAPI application structure for chat functionality
- Integrate OpenAI Agents SDK with proper configuration
- Establish basic request/response handling pipeline
- Derived from: [1-agent-specification.md](./1-agent-specification.md), [4-api-specification.md](./4-api-specification.md)

#### Expected Outcomes
- Basic `/api/{user_id}/chat` endpoint operational
- OpenAI Agent initialization framework
- Request/response serialization/deserialization
- Error handling middleware established

#### Directory Mapping
- **Location**: `backend/`
- **Components**:
  - `backend/api/v1/endpoints/chat.py` - Main chat endpoint
  - `backend/core/agents/chat_agent.py` - Agent initialization logic
  - `backend/schemas/chat.py` - Request/response schemas
  - `backend/middleware/auth.py` - Authentication middleware

#### Implementation Strategy
- Create dedicated modules for agent management
- Implement proper dependency injection for services
- Establish consistent error handling patterns

---

### Phase 2: Database Model Integration & Migrations

#### Objectives
- Implement SQLModel database models based on specification
- Create Alembic migration system for schema management
- Set up database session management
- Derived from: [5-database-model-specifications.md](./5-database-model-specifications.md)

#### Expected Outcomes
- Task, Conversation, Message models implemented
- Proper relationships and indexes configured
- Migration system operational
- Database session factory established

#### Directory Mapping
- **Location**: `backend/`
- **Components**:
  - `backend/models/task.py` - Task model with user relationships
  - `backend/models/conversation.py` - Conversation model
  - `backend/models/message.py` - Message model with tool execution data
  - `backend/database/session.py` - Database session management
  - `alembic/` - Migration files

#### Implementation Strategy
- Follow SQLModel patterns consistent with existing codebase
- Implement proper foreign key constraints
- Set up composite indexes as specified
- Create utility functions for common database operations

---

### Phase 3: MCP Server and Tool Implementation

#### Objectives
- Implement MCP server infrastructure using official SDK
- Create five specified MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Connect MCP tools to database models
- Derived from: [3-mcp-tool-specifications.md](./3-mcp-tool-specifications.md), [2-skills-sub-agent-design.md](./2-skills-sub-agent-design.md)

#### Expected Outcomes
- MCP server operational with registered tools
- All five task management tools implemented
- Tools properly integrated with database layer
- Input validation and error handling in place

#### Directory Mapping
- **Location**: `backend/`
- **Components**:
  - `backend/mcp/server.py` - MCP server implementation
  - `backend/mcp/tools/task_tools.py` - MCP task management tools
  - `backend/mcp/models.py` - MCP-specific data models
  - `backend/mcp/config.py` - MCP server configuration

#### Implementation Strategy
- Use official MCP SDK patterns for tool registration
- Implement proper input validation for each tool
- Ensure tools follow database transaction patterns
- Include proper error handling and logging

---

### Phase 4: Agent Initialization and Tool Wiring

#### Objectives
- Connect OpenAI Agent to MCP tools
- Implement agent initialization per request
- Wire agent skills to MCP tools
- Ensure proper authentication flows
- Derived from: [1-agent-specification.md](./1-agent-specification.md), [2-skills-sub-agent-design.md](./2-skills-sub-agent-design.md)

#### Expected Outcomes
- Agent properly initialized with MCP tools
- Skill mapping implemented per specifications
- Authentication context passed to agent
- Tool selection logic operational

#### Directory Mapping
- **Location**: `backend/`
- **Components**:
  - `backend/core/agents/todo_agent.py` - Main agent implementation
  - `backend/core/agents/skills.py` - Skill implementations
  - `backend/core/agents/intent_classifier.py` - Intent classification logic
  - `backend/core/agents/tool_wiring.py` - Agent-to-tool integration

#### Implementation Strategy
- Follow stateless pattern with full context reconstruction per request
- Implement proper tool calling and response handling
- Include conversation memory management
- Ensure proper user isolation

---

### Phase 5: Stateless Chat API Implementation

#### Objectives
- Implement complete stateless request lifecycle
- Create conversation persistence mechanism
- Implement message history loading and saving
- Ensure proper authentication and user isolation
- Derived from: [4-api-specification.md](./4-api-specification.md), [6-stateless-conversation-flow.md](./6-stateless-conversation-flow.md)

#### Expected Outcomes
- Complete request processing lifecycle implemented
- Database-backed conversation persistence
- Proper authentication and authorization
- API contract compliance verified

#### Directory Mapping
- **Location**: `backend/`
- **Components**:
  - `backend/api/v1/endpoints/chat.py` - Main chat endpoint logic
  - `backend/services/chat_service.py` - Conversation service
  - `backend/services/message_service.py` - Message persistence service
  - `backend/utils/conversation_loader.py` - Conversation history loader

#### Implementation Strategy
- Follow 6-step request lifecycle from specification
- Implement proper database transaction management
- Include conversation history optimization
- Ensure thread-safe operations

---

### Phase 6: Frontend ChatKit Integration

#### Objectives
- Implement OpenAI ChatKit integration
- Connect frontend to backend chat API
- Implement proper authentication flow
- Create user-friendly conversation interface
- Derived from: [7-frontend-chatkit-integration-spec.md](./7-frontend-chatkit-integration-spec.md)

#### Expected Outcomes
- Functional chat interface with ChatKit
- Proper authentication and user context
- Message display and input handling
- Error handling and user feedback

#### Directory Mapping
- **Location**: `frontend/`
- **Components**:
  - `frontend/components/TodoChat.jsx` - Main chat component
  - `frontend/lib/chat-api.js` - API client for chat endpoint
  - `frontend/context/ChatContext.jsx` - Chat context management
  - `frontend/pages/chat.jsx` - Chat page implementation

#### Implementation Strategy
- Follow Next.js 16+ patterns with App Router
- Implement proper state management
- Include responsive design considerations
- Ensure accessibility compliance

---

### Phase 7: Testing, Validation, and Readiness Checks

#### Objectives
- Implement comprehensive test suite
- Validate MCP tool correctness
- Test agent-to-tool interactions
- Verify stateless behavior and conversation continuity
- Derived from: All specification documents

#### Expected Outcomes
- Unit tests for all components
- Integration tests for API endpoints
- End-to-end tests for user flows
- Performance benchmarks established

#### Directory Mapping
- **Location**: `backend/` and `frontend/`
- **Components**:
  - `backend/tests/test_chat_api.py` - API integration tests
  - `backend/tests/test_mcp_tools.py` - MCP tool unit tests
  - `backend/tests/test_agent_integration.py` - Agent integration tests
  - `frontend/tests/test_chat_component.jsx` - Frontend component tests

#### Implementation Strategy
- Follow testing pyramid (unit > integration > e2e)
- Include mocking for external services
- Implement property-based testing where appropriate
- Include performance and stress testing

## Agent & MCP Integration Strategy

### OpenAI Agent Initialization
The agent will be initialized per request with complete conversation history loaded from the database. This ensures complete statelessness while maintaining conversational context. The agent will be configured with the MCP tools and appropriate system prompt from the agent specification.

### MCP Tool Registration
MCP tools will be registered dynamically with the server, allowing the agent to discover and use them during conversations. Each tool will follow the input/output schemas specified in the MCP tool specifications, with proper validation and error handling.

### Skill-to-Implementation Mapping
- **Task Management Skill** → MCP tool implementations
- **Intent Classification Skill** → Agent's built-in intent recognition
- **Conversation Context Skill** → Database loading/saving logic
- **Confirmation & UX Skill** → Response formatting and user interaction
- **Error Handling Skill** → Exception handling and error response formatting

### Statelessness Preservation
Each request will reconstruct the complete conversation context from the database, ensuring that server restarts don't affect conversation continuity. No in-memory state will be maintained between requests.

## Conversation Persistence Strategy

### Database Storage
Conversations and messages will be stored in the PostgreSQL database using the models specified. Each message will be persisted with proper user isolation through the user_id field.

### History Reconstruction
On each request, the system will load the most recent conversation history from the database, up to the configured maximum (default 50 messages), and reconstruct the conversation context for the agent.

### Restart Resilience
Since all state is stored in the database, server restarts will not affect conversation continuity. When a request comes in after a restart, the conversation will be loaded from the database as if there was no interruption.

## Authentication & User Isolation (JWT)

### JWT Integration
The system will leverage the existing Better Auth JWT implementation in the codebase. Authentication middleware will validate the JWT token and extract the user identity for scoping all operations.

### User Identity Derivation
The authenticated user ID will be extracted from the JWT claims and used to scope all database queries and operations. This ensures that users can only access their own data.

### User-Level Scoping Enforcement
- **Tasks**: All task operations filtered by user_id from JWT
- **Conversations**: All conversation access restricted to user's conversations
- **Messages**: All message operations scoped to user's conversation context

### Unauthorized Scenario Handling
Invalid or missing tokens will result in 401 Unauthorized responses. Expired tokens will trigger token refresh mechanisms where appropriate, or redirect to authentication flow for frontend requests.

## Testing & Validation Plan

### Required Test Types
- **Unit Tests**: Individual component functionality
- **Integration Tests**: API endpoint behavior with database
- **End-to-End Tests**: Complete user workflows
- **Performance Tests**: Load and stress testing
- **Security Tests**: Authentication and authorization validation

### Test Structure Reuse
Following the existing backend/frontend test structure in the codebase, with appropriate test organization and naming conventions.

### Validation Criteria
- **MCP Tool Correctness**: All tools follow specified input/output schemas and handle errors appropriately
- **Agent-to-Tool Interaction**: Agent properly invokes tools and processes results
- **Stateless Request Behavior**: Requests maintain independence and proper state reconstruction
- **Conversation Continuity**: Conversations resume correctly after server restarts

### Success Metrics
- All unit tests pass (>95% coverage target)
- Integration tests validate API contract compliance
- Performance benchmarks meet requirements
- Security scans pass without critical issues
- Manual testing confirms user experience meets specifications