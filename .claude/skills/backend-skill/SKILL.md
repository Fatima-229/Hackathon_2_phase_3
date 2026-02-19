---
name: backend-skill
description: Build backend systems by generating routes, handling requests and responses, and connecting to databases.
---

# Backend Development Skill

## Instructions

1. **Route Generation**
   - Define RESTful or RPC-style routes
   - Use clear and consistent URL naming
   - Separate public and protected routes
   - Apply proper HTTP methods (GET, POST, PUT, DELETE)

2. **Request Handling**
   - Parse request parameters, headers, and body
   - Validate and sanitize incoming data
   - Handle authentication and authorization
   - Manage middleware and request lifecycle

3. **Response Handling**
   - Return standardized response formats
   - Use appropriate HTTP status codes
   - Handle errors gracefully
   - Avoid leaking internal implementation details

4. **Database Connection**
   - Establish secure database connections
   - Use connection pooling where applicable
   - Perform CRUD operations safely
   - Handle database errors and timeouts

## Best Practices
- Keep controllers thin and logic modular
- Validate all incoming data
- Use environment variables for secrets
- Follow REST or API design standards consistently
- Log errors and important events
- Write reusable services and middleware

## Example Structure
```ts
// Route
app.post("/users", createUser);

// Controller
async function createUser(req, res) {
  const data = validate(req.body);
  const user = await db.user.create(data);
  return res.status(201).json(user);
}

// DB Connection
connectDatabase();
