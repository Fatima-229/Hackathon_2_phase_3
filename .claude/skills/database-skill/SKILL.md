---
name: database-skill
description: Design and manage databases including table creation, migrations, and schema design.
---

# Database Design Skill

## Instructions

1. **Schema Design**
   - Identify entities and relationships
   - Normalize data to reduce redundancy
   - Define primary and foreign keys
   - Choose appropriate data types

2. **Table Creation**
   - Create tables with clear naming conventions
   - Apply constraints (NOT NULL, UNIQUE, DEFAULT)
   - Use indexes for frequently queried fields
   - Ensure referential integrity

3. **Migrations**
   - Create versioned migration files
   - Support up and down migrations
   - Apply schema changes safely
   - Avoid destructive changes in production

4. **Database Structure**
   - Separate concerns (users, roles, logs, etc.)
   - Plan for scalability
   - Optimize for read/write performance
   - Maintain consistency across environments

## Best Practices
- Use migrations instead of manual schema edits
- Keep schemas simple and readable
- Never modify production data without backups
- Use snake_case or camelCase consistently
- Document schema changes clearly
- Test migrations before deployment

## Example Structure
```sql
-- Create table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Migration example
ALTER TABLE users
ADD COLUMN is_active BOOLEAN DEFAULT true;
