# Claude Code Agent Context: Todo Full-Stack Web Application

## Technologies in Use

### Frontend
- Next.js 16+ with App Router
- TypeScript 5.3+
- Tailwind CSS for styling
- Better Auth for authentication
- React Server Components and Client Components

### Backend
- Python 3.11+
- FastAPI for web framework
- SQLModel for ORM
- PyJWT for JWT handling
- python-jose for JWT verification

### Database
- Neon Serverless PostgreSQL
- UUID primary keys
- Proper indexing for performance

### Authentication Flow
- Better Auth handles user registration/login
- JWT tokens issued with 1-hour access token, 7-day refresh token
- Backend verifies JWT using shared secret
- User isolation through JWT-based scoping

## Key Implementation Notes

1. **Security**: All API endpoints require JWT in Authorization header
2. **User Isolation**: Backend extracts user ID from JWT and scopes all queries
3. **Frontend/Backend Separation**: Clear monorepo structure with dedicated directories
4. **API Client**: Centralized API client handles JWT inclusion and refresh
5. **Data Validation**: Client and server-side validation aligned with spec requirements