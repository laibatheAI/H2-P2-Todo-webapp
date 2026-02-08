# Skills & Sub-Agent Design: Todo AI Chatbot

## Overview

The Todo AI Chatbot implements a modular architecture with distinct skills that handle different aspects of task management and conversation flow. Each skill operates as a specialized sub-agent with clear boundaries and responsibilities.

## Skill Definitions

### 1. Task Management Skill

#### Purpose
Handles all CRUD operations for user tasks through MCP tools. This skill manages the actual task data operations.

#### Trigger Conditions
- User expresses intent to create, read, update, complete, or delete tasks
- Agent receives clear task management instruction from intent classification

#### Interaction with MCP Tools
- Calls `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task` MCP tools
- Validates input parameters before tool execution
- Processes tool responses for user-friendly presentation

#### Boundaries
- Does not handle conversation flow or user context
- Does not make decisions about tool chaining
- Does not handle authentication or user identification

### 2. Intent Classification Skill

#### Purpose
Analyzes user input to determine the specific action the user wants to perform and extracts relevant parameters.

#### Trigger Conditions
- New user message received
- Ambiguous user intent needs clarification

#### Interaction with MCP Tools
- Determines which MCP tool(s) should be called based on classified intent
- Extracts parameters needed for MCP tool calls
- Validates extracted parameters for completeness

#### Boundaries
- Does not execute MCP tools directly
- Does not maintain conversation state
- Does not generate user responses

### 3. Conversation Context Skill

#### Purpose
Manages conversation history and maintains context between user interactions. Handles message persistence and retrieval.

#### Trigger Conditions
- New user message received
- Agent response generated
- Conversation session begins or ends

#### Interaction with MCP Tools
- Does not directly interact with MCP tools
- Maintains conversation context that informs other skills
- Ensures conversation continuity across requests

#### Boundaries
- Does not interpret user intent
- Does not perform task operations
- Does not make decisions about tool usage

### 4. Confirmation & UX Skill

#### Purpose
Handles user experience aspects including confirmations, error messages, and helpful responses. Ensures human-friendly interaction.

#### Trigger Conditions
- Destructive operations are requested (delete, complete important tasks)
- User input is ambiguous or requires clarification
- Error conditions occur that need user guidance

#### Interaction with MCP Tools
- May trigger additional MCP tool calls for verification (e.g., listing tasks before deletion)
- Formats MCP tool responses for user consumption
- May intercept tool calls to request user confirmation

#### Boundaries
- Does not perform core task operations
- Does not manage conversation persistence
- Does not classify user intent

### 5. Error Handling Skill

#### Purpose
Manages error conditions and provides appropriate responses for various failure scenarios including task not found, invalid input, and authentication issues.

#### Trigger Conditions
- MCP tool execution fails
- Invalid user input detected
- Authentication/authorization issues arise
- System errors occur

#### Interaction with MCP Tools
- Intercepts MCP tool errors and generates appropriate user responses
- May retry operations with modified parameters
- Handles authentication renewal when needed

#### Boundaries
- Does not perform successful operations
- Does not manage normal conversation flow
- Does not interpret user intent for successful operations

## Skill Coordination

### Communication Pattern
Skills communicate through a shared context object that contains:
- User intent classification
- Extracted parameters
- Conversation history
- Current operation status
- Error states

### Execution Flow
1. Intent Classification Skill processes user input
2. Task Management Skill prepares and executes MCP tools
3. Conversation Context Skill updates message history
4. Confirmation & UX Skill formats responses
5. Error Handling Skill manages any failures in the process

## MCP Tool Integration Points

Each skill interacts with MCP tools through standardized interfaces:
- Input validation occurs in Intent Classification Skill
- Tool execution happens in Task Management Skill
- Response formatting handled by Confirmation & UX Skill
- Error handling managed by Error Handling Skill