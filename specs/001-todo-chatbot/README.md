# Todo AI Chatbot - Phase III Specification Overview

## Project Summary

The Todo AI Chatbot is a stateless conversational task management system that enables users to manage their tasks through natural language interactions. The system uses OpenAI Agents SDK with MCP tools to perform task operations while maintaining all state in a database.

## Architecture Overview

The system consists of seven main specification components:

1. **[Agent Specification](./1-agent-specification.md)** - Defines the role, responsibilities, and behavior of the Todo AI Agent
2. **[Skills & Sub-Agent Design](./2-skills-sub-agent-design.md)** - Details the modular skill architecture
3. **[MCP Tool Specifications](./3-mcp-tool-specifications.md)** - Specifies the available MCP tools for task management
4. **[API Specification](./4-api-specification.md)** - Defines the stateless API endpoint and contracts
5. **[Database Model Specifications](./5-database-model-specifications.md)** - Details the data models and relationships
6. **[Stateless Conversation Flow](./6-stateless-conversation-flow.md)** - Outlines the request processing lifecycle
7. **[Frontend (ChatKit) Integration](./7-frontend-chatkit-integration-spec.md)** - Specifies the frontend integration requirements

## Technology Stack

- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **Frontend**: OpenAI ChatKit
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth
- **Architecture**: Stateless, server-side persistence

## Key Features

- Natural language task management
- Complete statelessness with database persistence
- MCP tool integration for task operations
- User-isolated data and conversations
- Conversational context maintenance
- Error handling and recovery
- Frontend integration with ChatKit

## Success Criteria

- Natural language task management works end-to-end via MCP tools
- Agent correctly selects and chains MCP tools based on user intent
- Conversation state is persisted and resumes after server restarts
- MCP tools are stateless and database-backed
- Specs are deterministic, unambiguous, and Claude-Code executable
- Clear separation of concerns between agent logic, tools, API, and database