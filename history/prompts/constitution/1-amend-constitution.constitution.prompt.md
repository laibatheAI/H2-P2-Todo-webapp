---
id: 1
title: Amend Constitution
stage: constitution
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user:
command: /sp.constitution
labels: [constitution,spec-driven-development,full-stack]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
---

## Prompt

```text
```Project: Phase II – Todo Full-Stack Web Application (Hackathon II)

Objective:
Transform an existing console-based Todo application into a modern, multi-user, full-stack web application using a strict spec-driven and agentic development workflow powered by Spec-Kit Plus and Claude Code.

Core principles:
- Spec-driven development (no implementation without approved specs)
- Zero manual coding (all code generated via Claude Code)
- Security-first design (JWT-based authentication and user isolation)
- Clear separation of concerns (frontend, backend, database)
- Reproducibility (all changes traceable to specs and prompts)

Development standards:
- Follow Agentic Dev Stack workflow strictly:
  Write spec → Generate plan → Break into tasks → Implement via Claude Code
- Claude Code must always reference relevant specs using @specs/ paths
- Any change in behavior must be reflected in spec updates first
- Frontend and backend must be implemented within a single monorepo context

Technology constraints:
- Frontend: Next.js 16+ (App Router, TypeScript, Tailwind CSS)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Spec System: GitHub Spec-Kit Plus + Claude Code

API standards:
- RESTful API design under `/api/`
- All endpoints must require a valid JWT token
- JWT must be passed via `Authorization: Bearer <token>` header
- Backend must verify JWT using shared secret (`BETTER_AUTH_SECRET`)
- All task queries must be filtered by authenticated user ID
- Unauthorized requests must return `401 Unauthorized`

Authentication rules:
- User signup/signin handled on frontend using Better Auth
- Backend must not trust frontend user IDs without JWT verification
- Task ownership must be enforced on every CRUD operation
- Users can only view, modify, or delete their own tasks

Database rules:
- Persistent storage using Neon PostgreSQL
- Tasks must be associated with authenticated users
- No shared task visibility across users
- Database schema must match `/specs/database/schema.md`

Frontend standards:
- Responsive UI for desktop and mobile
- Use server components by default
- Client components only for interactivity
- All API calls must go through a centralized API client
- No direct backend calls outside the API client layer

Repository organization:
- Monorepo structure is mandatory
- Specs must reside in `/specs/` following Spec-Kit conventions
- Separate `CLAUDE.md` files for root, frontend, and backend
- Claude Code must respect folder-specific guidelines

Constraints:
- No manual code edits allowed
- No deviation from approved tech stack
- No hardcoded secrets in code
- Environment variables must be used for secrets and URLs

Success criteria:
- All Phase II basic features implemented as a web application
- Secure multi-user authentication with JWT
- Each user only accesses their own tasks
- Backend, frontend, and database fully integrated
- All implementation steps traceable to specs and Claude Code prompts
- Project passes review based on process, specs, and iterations ```
```

## Response snapshot

The constitution file at `.specify/memory/constitution.md` has been successfully updated to reflect the requirements for transforming the Todo application from a console-based app to a full-stack web application.

Key changes made:
- Updated project name from "Todo In-Memory Python Console App" to "Todo Full-Stack Web Application"
- Revised all 6 core principles to align with full-stack web application development
- Added new sections for API Standards, Authentication Rules, Database Rules, and Frontend Standards
- Updated constraints to reflect the new technology stack (Next.js 16+, Python FastAPI, SQLModel, Neon PostgreSQL, Better Auth)
- Modified development workflow to emphasize spec-driven and agentic development
- Version incremented from 1.0.0 to 2.0.0 with proper governance information
- Created comprehensive sync impact report documenting all changes

The updated constitution now properly reflects the project's transformation from a simple console application to a modern, multi-user, full-stack web application with JWT-based authentication, proper separation of concerns, and adherence to the agentic development workflow.

## Outcome

- ✅ Impact: Constitution updated to reflect full-stack web application requirements (v1.0.0 → v2.0.0)
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Updated .specify/memory/constitution.md with new principles and constraints
- 🔁 Next prompts: Plan and spec creation for frontend and backend components
- 🧠 Reflection: Constitution now properly guides the transformation from console app to full-stack web application

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create feature specifications based on updated constitution