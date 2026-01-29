<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles: All 6 principles updated for full-stack web application
- Added sections: API Standards, Authentication Rules, Database Rules, Frontend Standards
- Removed sections: Console-specific principles
- Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development (SDD) Foundation
No code generation without a validated spec, plan, and tasks. All implementation must be traceable back to formal specifications with no manual coding allowed. This ensures transparency and traceability of all decisions and code. All development follows the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.

### AI-Native Workflow
Use Claude Code exclusively for implementation, with iterative spec refinement until output matches requirements. All development tasks must be executed through Spec-Kit Plus and Claude Code tools only. Claude Code must always reference relevant specs using @specs/ paths, and any change in behavior must be reflected in spec updates first.

### Security-First Design
Implement JWT-based authentication and strict user isolation. All API endpoints must require valid JWT tokens, enforce user ownership of data, and prevent unauthorized access. Backend must verify JWT using shared secret and all task queries must be filtered by authenticated user ID.

### Clear Separation of Concerns
Maintain distinct frontend, backend, and database layers within a single monorepo context. Frontend (Next.js 16+) handles user interface and authentication, backend (Python FastAPI) manages business logic and data access, and database (Neon PostgreSQL) provides persistent storage with proper user isolation.

### Reproducibility and Traceability
All changes must be traceable to specs and prompts with complete audit trail from requirements to implementation. Every development activity must be documented and linked back to formal specifications. Maintain clear compliance reviews to ensure adherence to these principles.

### Full-Stack Integration
Ensure seamless integration between frontend, backend, and database components. Implement centralized API client for all communication, maintain consistent data models across layers, and provide responsive UI for both desktop and mobile experiences.

## API Standards

- RESTful API design under `/api/`
- All endpoints must require a valid JWT token
- JWT must be passed via `Authorization: Bearer <token>` header
- Backend must verify JWT using shared secret (`BETTER_AUTH_SECRET`)
- All task queries must be filtered by authenticated user ID
- Unauthorized requests must return `401 Unauthorized`

## Authentication Rules

- User signup/signin handled on frontend using Better Auth
- Backend must not trust frontend user IDs without JWT verification
- Task ownership must be enforced on every CRUD operation
- Users can only view, modify, or delete their own tasks

## Database Rules

- Persistent storage using Neon PostgreSQL
- Tasks must be associated with authenticated users
- No shared task visibility across users
- Database schema must match `/specs/database/schema.md`

## Constraints

Technology Stack: Frontend: Next.js 16+ (App Router, TypeScript, Tailwind CSS), Backend: Python FastAPI, ORM: SQLModel, Database: Neon Serverless PostgreSQL, Authentication: Better Auth with JWT, Spec System: GitHub Spec-Kit Plus + Claude Code. Repository: Monorepo structure is mandatory, Specs must reside in `/specs/` following Spec-Kit conventions. No manual code edits allowed, No deviation from approved tech stack, No hardcoded secrets in code, Environment variables must be used for secrets and URLs.

## Frontend Standards

- Responsive UI for desktop and mobile
- Use server components by default
- Client components only for interactivity
- All API calls must go through a centralized API client
- No direct backend calls outside the API client layer

## Development Workflow

Code Quality: Follow Next.js/TypeScript best practices for frontend, PEP 8 style guide for Python backend, use type hints, include docstrings for functions/classes, and ensure readability. Project Structure: Monorepo with /src for application code, /specs for all specification files, Constitution file, README.md, and CLAUDE.md. Testing: Include comprehensive unit and integration tests to ensure functionality across all layers. Documentation: README.md must include setup instructions, CLAUDE.md must guide Claude Code usage for both frontend and backend development.

## Governance

This constitution serves as the governing document for the Todo Full-Stack Web Application project. All development activities must comply with these principles. Amendments to this constitution require formal documentation and approval process. Version control and compliance reviews will be conducted to ensure adherence to these principles.

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-06
