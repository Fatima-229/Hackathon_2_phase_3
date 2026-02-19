# Todo Full-Stack Web Application — Phase III: AI Chatbot

## Overview
This is a full-stack todo application featuring an AI-powered chatbot that allows users to manage their tasks using natural language. The application includes authentication, task management, and an intelligent assistant that can perform all task operations through conversation.

## Features
- User authentication and authorization
- Task management (create, read, update, delete, mark as complete)
- AI-powered chatbot for task management using natural language
- Responsive, mobile-first design with dark mode
- Conversation history persistence

## Tech Stack
- **Frontend**: Next.js 14+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **Database**: SQLModel with SQLite (with PostgreSQL support)
- **Authentication**: JWT-based authentication
- **AI Integration**: OpenAI GPT with function calling
- **MCP Tools**: Custom tools for task operations

## Architecture
- **Frontend**: Next.js app with React components
- **Backend**: FastAPI with modular API routes
- **AI Layer**: OpenAI integration with custom tools
- **Database**: SQLModel ORM with conversation and message persistence

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
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

5. Set up environment variables by copying `.env.example` to `.env` and filling in the values:
   ```bash
   # Database Configuration
   DATABASE_URL="sqlite:///./todo_app.db"

   # JWT settings
   JWT_SECRET_KEY="your-super-secret-jwt-key-here-make-it-long-and-random"
   JWT_ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days

   # API Configuration
   API_HOST="0.0.0.0"
   API_PORT=8000

   # OpenAI API Key
   OPENAI_API_KEY="your-openai-api-key-here"
   ```

6. Run the backend server:
   ```bash
   python run_server.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables by creating a `.env.local` file:
   ```bash
   NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1"
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## AI Chatbot Features
The AI chatbot allows users to manage their tasks using natural language. Supported commands include:

- "Add a task to buy groceries"
- "Show me my tasks"
- "Complete task with ID 123"
- "Update task with ID 123 to have a high priority"
- "Delete task with ID 123"

The AI uses MCP (Model Context Protocol) tools to perform these operations securely and maintains conversation context in the database.

## API Endpoints
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/tasks` - Get user's tasks
- `POST /api/v1/tasks` - Create a new task
- `PUT /api/v1/tasks/{id}` - Update a task
- `DELETE /api/v1/tasks/{id}` - Delete a task
- `PATCH /api/v1/tasks/{id}/complete` - Toggle task completion
- `POST /api/v1/chat/{user_id}` - Chat with AI assistant

## Project Structure
```
hackathon_2_phase_3/
├── backend/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── tasks.py
│   │       └── chat.py
│   ├── models/
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── mcp/
│   │   ├── server.py
│   │   └── tools.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   └── chat/
│   ├── components/
│   │   ├── AuthProvider.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── ChatInput.tsx
│   │   ├── ChatHeader.tsx
│   │   └── Navbar.tsx
│   └── constants/
│       └── api.ts
├── sp.constitution
├── sp.specify
├── sp.plan
├── sp.generate
├── sp.tasks
└── README.md
```

## Phase III Implementation
This Phase III implementation adds an AI-powered chatbot to the existing todo application. The chatbot uses OpenAI's GPT model with function calling to perform task operations through natural language. The system maintains conversation history in the database and ensures all operations are properly authenticated and authorized.

## Specifications
- **sp.constitution**: Core principles and constraints
- **sp.specify**: Detailed feature specifications
- **sp.plan**: Implementation plan
- **sp.generate**: Generation instructions
- **sp.tasks**: Granular implementation tasks"# Hackathon_2_phase_3" 
