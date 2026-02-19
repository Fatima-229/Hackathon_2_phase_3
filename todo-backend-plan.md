# Todo Full-Stack Web Application – Backend & API Implementation Plan

## Objective
Implement a fully functional RESTful API backend for the Todo app with secure JWT authentication and persistent storage

## Target Audience
Developers and testers validating API functionality and data persistence

## Focus
Correct API behavior, secure user access, and database integration

## Success Criteria
- Implements all RESTful endpoints: GET, POST, PUT, DELETE, PATCH for tasks
- JWT verification middleware validates all requests
- Users can only access their own tasks
- API responses return correct HTTP status codes (200, 201, 401, 404)
- Tasks stored persistently in Neon Serverless PostgreSQL using SQLModel ORM
- Error handling and validations implemented for all endpoints
- End-to-end integration tested with frontend (Spec 1)

## Constraints
- Technology stack: FastAPI + SQLModel ORM
- JWT secret must match frontend Better Auth configuration (BETTER_AUTH_SECRET)
- No manual coding; implement via Claude Code and Spec-Kit Plus
- Follow Agentic Dev Stack workflow: spec → plan → tasks → implementation
- Timeline: Complete Spec 2 within 4-5 days

## Not Building
- Frontend interface or styling
- Advanced analytics, reporting, or notifications
- Non-task-related backend features (e.g., logging unrelated services)

## Implementation Plan

### Phase 1: Project Setup and Dependencies
1. Initialize FastAPI project structure
2. Install required packages: FastAPI, SQLModel, Neon connector, JWT libraries
3. Configure environment variables for database connection and JWT secret
4. Set up project directory structure

### Phase 2: Database Models and Schema
1. Define User model using SQLModel
2. Define Task model with relationships to User
3. Create database tables and relationships
4. Implement database session management

### Phase 3: Authentication System
1. Integrate Better Auth or implement custom JWT authentication
2. Create middleware for JWT token verification
3. Implement user registration and login endpoints
4. Ensure JWT secret matches frontend configuration

### Phase 4: Core API Endpoints
1. Implement GET /api/tasks - Retrieve user's tasks with filtering
2. Implement POST /api/tasks - Create new task for authenticated user
3. Implement GET /api/tasks/{id} - Retrieve specific task
4. Implement PUT /api/tasks/{id} - Update specific task
5. Implement DELETE /api/tasks/{id} - Delete specific task
6. Implement PATCH /api/tasks/{id}/complete - Toggle task completion

### Phase 5: Security and Validation
1. Implement user data isolation (users can only access their own tasks)
2. Add request validation using Pydantic models
3. Implement proper error handling with appropriate HTTP status codes
4. Add rate limiting if necessary

### Phase 6: Testing and Integration
1. Write unit tests for all endpoints
2. Perform integration testing with sample data
3. Validate end-to-end flow with frontend
4. Test error conditions and edge cases

## Detailed Technical Steps

### 1. Project Structure
```
backend/
├── main.py                 # FastAPI app entry point
├── config.py              # Configuration and settings
├── database.py            # Database setup and session management
├── models/
│   ├── __init__.py
│   ├── user.py           # User model
│   └── task.py           # Task model
├── schemas/
│   ├── __init__.py
│   ├── user.py           # User Pydantic schemas
│   └── task.py           # Task Pydantic schemas
├── api/
│   ├── __init__.py
│   ├── deps.py           # Dependency injection
│   └── v1/
│       ├── __init__.py
│       ├── auth.py       # Authentication endpoints
│       └── tasks.py      # Task endpoints
├── utils/
│   ├── __init__.py
│   ├── auth.py          # Authentication utilities
│   └── security.py      # Security utilities
└── tests/
    ├── __init__.py
    ├── conftest.py      # Test configuration
    ├── test_auth.py     # Authentication tests
    └── test_tasks.py    # Task endpoint tests
```

### 2. Database Models
- User model with id, email, hashed_password, created_at
- Task model with id, title, description, completed, priority, due_date, user_id, created_at, updated_at
- Proper foreign key relationship between Task and User

### 3. API Endpoints Specification
- GET /api/v1/tasks - Get all tasks for authenticated user (with optional filters)
  - Query params: completed (boolean), priority (enum), limit, offset
  - Response: 200 OK with array of tasks
- POST /api/v1/tasks - Create new task for authenticated user
  - Request body: {title, description?, completed?, priority?, due_date?}
  - Response: 201 Created with created task
- GET /api/v1/tasks/{id} - Get specific task
  - Response: 200 OK with task object or 404 if not found
- PUT /api/v1/tasks/{id} - Update specific task
  - Response: 200 OK with updated task or 404 if not found
- DELETE /api/v1/tasks/{id} - Delete specific task
  - Response: 204 No Content or 404 if not found
- PATCH /api/v1/tasks/{id}/complete - Toggle task completion
  - Response: 200 OK with updated task or 404 if not found

### 4. Authentication Flow
- Middleware extracts JWT from Authorization header
- Verifies token using BETTER_AUTH_SECRET
- Extracts user ID from token payload
- Attaches user info to request context
- All endpoints validate that user owns the resource being accessed

### 5. Error Handling
- Custom exception handlers for common errors
- Consistent error response format
- Proper HTTP status codes for all scenarios
- Logging for debugging purposes

## Implementation Timeline
- Day 1: Project setup, dependencies, and database models
- Day 2: Authentication system and middleware
- Day 3: Core API endpoints implementation
- Day 4: Security, validation, and testing
- Day 5: Integration testing and documentation