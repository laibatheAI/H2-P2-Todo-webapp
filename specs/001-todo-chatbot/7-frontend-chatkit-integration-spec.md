# Frontend (ChatKit) Integration Spec: Todo AI Chatbot

## Overview

This document specifies the integration requirements for the OpenAI ChatKit frontend component to work with the Todo AI Chatbot backend. The integration ensures seamless message exchange and proper handling of the conversational AI experience.

## Message Exchange Expectations

### Outgoing Messages (User to Server)
- User messages sent as plain text in the request body
- Messages include proper authentication headers with JWT
- Client sends user_id as part of the endpoint path
- Messages may include metadata about the client environment

### Incoming Messages (Server to User)
- Assistant responses returned as formatted text
- Tool execution results embedded in response when applicable
- System messages (like confirmations) formatted consistently
- Error messages presented in user-friendly format

### Message Formatting
- User messages: Plain text input from ChatKit
- Assistant messages: Rich text with potential tool call indicators
- System messages: Clearly distinguishable from user/assistant messages
- Error messages: Human-readable with suggestions for resolution

## Domain Allowlist Requirements

### Allowed Origins
- Production: `https://yourdomain.com`
- Staging: `https://staging.yourdomain.com`
- Development: `http://localhost:3000`
- Preview deployments as needed

### API Endpoint Access
- Allow access to `/api/:user_id/chat` endpoint
- Configure CORS to accept requests from allowed origins
- Permit authentication headers to be sent with requests
- Allow JSON content type for request/response bodies

### Security Headers
- Enable strict transport security (HSTS)
- Configure content security policy (CSP) appropriately
- Allow necessary third-party resources for ChatKit functionality
- Block unsafe inline scripts and styles

## Environment Variables Usage

### Required Environment Variables
- `NEXT_PUBLIC_CHATKIT_SERVER_URL`: Base URL for the chat API
- `NEXT_PUBLIC_JWT_TOKEN_STORAGE_KEY`: Key for storing JWT in browser storage
- `NEXT_PUBLIC_DEFAULT_USER_ID`: Default user ID for development (optional)

### Optional Environment Variables
- `NEXT_PUBLIC_CHATKIT_THEME`: Theme configuration for ChatKit UI
- `NEXT_PUBLIC_API_RATE_LIMIT_DELAY`: Delay between requests to respect rate limits
- `NEXT_PUBLIC_MAX_CONVERSATION_HISTORY`: Maximum messages to display in UI

### Configuration Variables
- `CHATKIT_DOMAIN_ALLOWLIST`: Comma-separated list of allowed domains
- `JWT_EXPIRATION_BUFFER_MS`: Buffer time before token expiration for refresh
- `CONVERSATION_POLLING_INTERVAL`: Interval for polling for new messages if needed

## Chat Session Handling

### Session Initialization
- Load existing conversation history from server on initial load
- Display welcome message or last conversation context
- Initialize ChatKit with proper authentication
- Set up event listeners for message events

### User Authentication Flow
- Redirect to login if JWT is not present or expired
- Refresh JWT tokens before making API calls when near expiration
- Handle authentication failures gracefully
- Clear session data on logout

### Conversation Continuity
- Maintain conversation context across page refreshes
- Store conversation ID in browser storage if needed
- Resume conversations from last known state
- Handle disconnection and reconnection scenarios

### Message Streaming Simulation
- Show typing indicators when awaiting server response
- Handle tool execution delays appropriately
- Display partial responses if streaming becomes available
- Manage message ordering during asynchronous operations

## Error Handling and User Experience

### Network Error Handling
- Display user-friendly messages for network failures
- Implement retry logic for transient failures
- Show appropriate offline indicators
- Cache pending messages for retry when connection restored

### API Error Handling
- Differentiate between client and server errors
- Show validation errors in context of user input
- Handle rate limiting with appropriate user messaging
- Manage authentication expiration seamlessly

### Tool Execution Feedback
- Indicate when MCP tools are being executed
- Show progress indicators for longer operations
- Display tool results in context of conversation
- Handle tool execution failures gracefully

## Performance Optimizations

### Message History Management
- Implement virtual scrolling for long conversations
- Paginate history loading for very long conversations
- Cache recent conversation history in browser
- Lazy load older messages when needed

### Resource Optimization
- Minimize bundle size for ChatKit integration
- Optimize image and asset loading
- Implement efficient rendering of message lists
- Use appropriate compression for API requests

### Connection Management
- Maintain persistent connections where beneficial
- Implement proper cleanup of connection resources
- Handle multiple simultaneous requests appropriately
- Optimize connection pooling for API calls

## Accessibility and Internationalization

### Accessibility Compliance
- Ensure ChatKit components meet WCAG standards
- Support screen readers and keyboard navigation
- Provide appropriate ARIA labels and roles
- Maintain color contrast ratios for accessibility

### Localization Support
- Prepare for internationalization of system messages
- Support right-to-left languages if applicable
- Handle date/time formatting for different locales
- Allow for text expansion in translated messages