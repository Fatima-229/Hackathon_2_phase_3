---
name: auth-skill
description: Implement secure authentication systems including signup, sign in, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Validate user input (email, password, username)
   - Enforce strong password rules
   - Prevent duplicate accounts
   - Store users securely in the database

2. **Password Hashing**
   - Use industry-standard hashing (bcrypt, argon2, or scrypt)
   - Apply proper salting
   - Never store plaintext passwords
   - Verify passwords securely during login

3. **User Sign In**
   - Authenticate using email/username + password
   - Handle invalid credentials safely
   - Prevent timing attacks
   - Return appropriate error messages (generic, non-revealing)

4. **JWT Authentication**
   - Generate access tokens on successful login
   - Include minimal, non-sensitive payload data
   - Set token expiration times
   - Verify JWTs for protected routes

5. **Better Auth Integration**
   - Configure Better Auth providers
   - Integrate with existing user models
   - Handle session management
   - Support token-based and session-based auth if needed

## Best Practices
- Always hash passwords before storage
- Use HTTPS for all auth-related requests
- Keep JWT secrets secure and environment-based
- Rotate secrets periodically
- Implement refresh tokens if applicable
- Log auth events without sensitive data

## Example Structure
```ts
// Signup
const hashedPassword = await hash(password);
await db.user.create({
  email,
  password: hashedPassword,
});

// Login
const isValid = await verify(password, user.password);
if (!isValid) throw new Error("Invalid credentials");

// JWT
const token = signJwt({ userId: user.id });

// Protected route
verifyJwt(token);
