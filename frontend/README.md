# Todo Full-Stack Web Application - Frontend

This is the frontend component of the Todo Full-Stack Web Application, built with Next.js 16+ and React.

## Features

- **Authentication**: Login and signup pages with JWT token management
- **Task Management**: Full CRUD operations for tasks
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Reusable Components**: TaskList, TaskCard, CreateTask, UpdateTask
- **Secure API Integration**: JWT tokens attached to all API requests
- **Neon Console Integration**: Server-side functions for direct database operations

## Tech Stack

- Next.js 16+ (App Router)
- React 19+
- TypeScript
- Tailwind CSS
- Server Actions for secure database operations

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── auth/              # Authentication pages
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/         # Main dashboard page
│   ├── admin/             # Neon console integration page
│   ├── layout.tsx         # Root layout with AuthProvider
│   └── page.tsx           # Home page with auth redirect
├── components/            # Reusable React components
│   ├── AuthProvider.tsx   # Authentication context
│   ├── Navbar.tsx         # Navigation component
│   ├── TaskList.tsx       # Task list component
│   ├── TaskCard.tsx       # Individual task card
│   ├── CreateTask.tsx     # Task creation form
│   └── ProtectedRoute.tsx # Protected route wrapper
├── utils/                 # Utility functions
│   ├── fetchClient.ts     # API client with JWT handling
│   └── taskAPI.ts         # Task API service
├── actions/               # Server actions
│   └── taskActions.ts     # Server-side task operations
└── package.json           # Dependencies
```

## Key Implementation Details

### Authentication
- JWT tokens are stored in localStorage
- AuthProvider context manages authentication state
- Protected routes redirect unauthenticated users
- Tokens are automatically attached to API requests

### API Integration
- `fetchClient.ts` handles JWT token attachment
- `taskAPI.ts` provides all task-related API methods
- All API calls are properly typed with TypeScript interfaces

### Neon Console Integration
- Server actions in `actions/taskActions.ts` handle secure database operations
- Direct database access happens server-side, keeping credentials secure
- Available at `/admin` for administrative/testing purposes

## Environment Variables

Create a `.env.local` file in the frontend directory with the following content:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

Update the `NEXT_PUBLIC_API_URL` value if your backend is running on a different port or URL.

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. The application will be available at `http://localhost:3000`

## Security Features

- JWT tokens are securely stored and transmitted
- User isolation: each user can only access their own tasks
- Server-side database operations keep credentials secure
- Protected routes prevent unauthorized access
- Input validation and sanitization

## Responsive Design

The UI is designed to work across all device sizes:
- Mobile-first approach
- Responsive grid layouts
- Adaptive component sizing
- Touch-friendly controls