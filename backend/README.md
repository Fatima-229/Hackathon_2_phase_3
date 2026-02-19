# Todo API Backend

The Todo API backend is built with FastAPI and provides endpoints for user authentication and task management.

## Features

- User registration and authentication
- Task creation, retrieval, updating, and deletion
- Task filtering and pagination
- Secure password hashing with Argon2
- JWT-based authentication

## Prerequisites

- Python 3.8+
- pip

## Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (if not already created):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables by copying `.env.example` to `.env` and updating the values as needed:
   ```bash
   copy .env.example .env  # On Windows
   # Or
   cp .env.example .env    # On macOS/Linux
   ```

## Running the Server

### Method 1: Using the run script (recommended)
```bash
python run_server.py
```

### Method 2: Direct execution
```bash
python main.py
```

### Method 3: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000` by default.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Available Endpoints

- `GET /` - Health check endpoint
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login an existing user
- `GET /api/v1/tasks/` - Get all tasks for the authenticated user
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a specific task
- `DELETE /api/v1/tasks/{task_id}` - Delete a specific task
- `PATCH /api/v1/tasks/{task_id}/complete` - Toggle task completion status

## Database

The application uses PostgreSQL as the primary database. The connection string is configured in the `.env` file via the `DATABASE_URL` variable. For development, it defaults to a local SQLite database.

## Testing

To run the tests:
```bash
pytest
```

Or for more verbose output:
```bash
pytest -v
```