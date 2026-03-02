# JustNotes

A simple, secure note-taking API built with FastAPI and SQLModel, featuring JWT authentication and a well-organized codebase.

## Features

- **JWT Authentication** - Secure user authentication with JSON Web Tokens
- **Note Management** - Create, read, and update notes with ownership control
- **Public Notes** - Share notes publicly while keeping private notes secure
- **User System** - User registration and management with password hashing
- **RESTful API** - Clean, documented API endpoints
- **SQLite Database** - Lightweight database with SQLModel ORM
- **Auto Documentation** - Interactive API docs at `/docs`

## Project Structure

```
src/
├── api/                    # API endpoints
│   ├── auth.py            # Authentication endpoints (login, user info)
│   ├── notes.py           # Note CRUD operations
│   ├── users.py           # User management
│   └── health.py          # Health check endpoint
├── models/                 # Data models
│   ├── note.py            # Note models (Note, NoteBase, NoteResponse)
│   └── user.py            # User models (User, UserBase, UserResponse)
├── database/              # Database layer
│   ├── connection.py      # Database connection and session management
│   └── crud.py            # CRUD operations for notes and users
├── utils/                 # Utility functions
│   ├── auth.py            # Password hashing and verification
│   └── jwt.py             # JWT token creation and verification
├── config/                # Configuration
│   └── settings.py        # Application settings and environment variables
└── main.py               # FastAPI app setup and router registration
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /auth/login` - User login and JWT token generation
- `GET /auth/me` - Get current user information (requires authentication)

### Users
- `POST /user/create` - Create a new user account
- `GET /user/list` - List all users (requires authentication)

### Notes
- `GET /notes` - Get all notes (requires authentication)
- `POST /notes/create` - Create a new note (requires authentication)
- `GET /notes/{id}` - Get a specific note (requires authentication, ownership check)
- `PUT /notes/{id}` - Update a note (requires authentication, ownership required)
- `GET /notes/public` - Get all public notes (no authentication required)

### Health
- `GET /health` - Health check endpoint

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Create a user**: `POST /user/create`
2. **Login to get token**: `POST /auth/login` with form data `username` and `password`
3. **Use the token**: Include `Authorization: Bearer <token>` header in protected requests

Tokens expire after 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`).

## Security Features

- **Password Hashing** - Uses bcrypt for secure password storage
- **JWT Tokens** - Secure token-based authentication
- **Ownership Control** - Users can only modify their own notes
- **Public/Private Notes** - Granular access control for note visibility
- **Input Validation** - Pydantic models for request/response validation

## Configuration

The application uses environment variables for configuration. Create a `.env` file:

```env
DATABASE_URL=sqlite:///db.sqlite
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=JustNotes
APP_VERSION=0.0.1
APP_DESCRIPTION=JustNotes is a simple note-taking app
```

## Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Development

The codebase follows FastAPI best practices with:
- Separation of concerns (API, models, database, utils)
- Dependency injection for database sessions
- Comprehensive documentation and type hints
- Clean architecture with modular components

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.