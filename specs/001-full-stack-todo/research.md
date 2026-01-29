# Research: Todo Full-Stack Web Application

**Feature**: 001-full-stack-todo
**Date**: 2026-01-06

## Architectural Decisions

### JWT Verification Approach

**Decision**: Symmetric signing using shared secret (`BETTER_AUTH_SECRET`)
**Rationale**: Better Auth uses symmetric signing by default with a shared secret. This is simpler to implement and sufficient for our monolithic application architecture. The shared secret will be stored in environment variables as required by the constitution.
**Alternatives considered**:
- Asymmetric signing (RS256 / EdDSA with JWKS endpoint): More complex setup, but better for distributed systems where the public key needs to be shared with multiple services. Not necessary for our single backend application.

### API Path Design

**Decision**: Using `/api/tasks` endpoints with JWT-based user scoping
**Rationale**: This follows RESTful conventions and leverages JWT claims to identify the user, eliminating the need for explicit user identifiers in URLs. The backend will extract the user ID from the JWT and scope all queries to that user.
**Alternatives considered**:
- Explicit user identifiers in URLs (`/api/users/{id}/tasks`): Would require additional validation to ensure users can't access other users' data by manipulating the URL. JWT-based scoping is more secure.

### Frontend-Backend Communication Strategy

**Decision**: Centralized API client with proper error handling and JWT token management
**Rationale**: This aligns with frontend standards in the constitution (all API calls through centralized client, no direct backend calls). The API client will handle JWT token inclusion in headers and refresh expired tokens.
**Alternatives considered**:
- Direct API calls from components: Would lead to code duplication and inconsistent error handling across the application.

## Technology Research Findings

### Better Auth Integration

Better Auth provides a complete authentication solution that handles user registration, login, and JWT token issuance. It integrates well with Next.js applications and provides middleware for both client and server components.

### FastAPI JWT Verification

FastAPI can verify JWT tokens using libraries like `python-jose` or `PyJWT`. The backend will extract user information from the token payload and validate the token signature using the shared secret.

### SQLModel for Database Operations

SQLModel is the perfect ORM choice as it combines SQLAlchemy and Pydantic, allowing for consistent data models between the API layer and database layer. It supports async operations which is important for performance.

## Security Considerations

### Token Storage and Transmission

- JWT tokens will be stored in httpOnly cookies when possible for XSS protection
- For API calls, tokens will be transmitted via Authorization header as required by the specification
- Refresh tokens will be used to maintain user sessions without requiring frequent re-authentication

### User Isolation

- All database queries will be scoped by the authenticated user ID extracted from the JWT
- The backend will never trust user IDs passed from the frontend without JWT verification
- Proper authorization checks will be implemented at the API level to prevent cross-user data access