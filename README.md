# JustNotes

A simple, secure note-taking API built with FastAPI and SQLModel, featuring JWT authentication, AI-powered features, and a well-organized codebase.

## Features

### Core Features
- **JWT Authentication** - Secure user authentication with JSON Web Tokens
- **Note Management** - Create, read, update, and delete notes with ownership control
- **Public Notes** - Share notes publicly while keeping private notes secure
- **User System** - User registration and management with password hashing
- **Tag & Keyword System** - Organize notes with tags and keywords
- **RESTful API** - Clean, documented API endpoints
- **SQLite Database** - Lightweight database with SQLModel ORM
- **Auto Documentation** - Interactive API docs at `/docs`

### AI-Powered Features
- **Auto-Summarize** - Generate concise summaries of your notes
- **Content Extension** - Expand notes with AI-generated insights
- **Translation** - Translate notes to any language
- **Auto-Tagging** - AI suggests relevant tags and categories
- **Keyword Extraction** - Automatically extract key terms and topics
- **Sentiment Analysis** - Analyze emotional tone of notes
- **Related Notes** - Find connections between your notes

## Project Structure

```
src/
├── api/                    # API endpoints
│   ├── auth.py            # Authentication endpoints (login, user info)
│   ├── notes.py           # Note CRUD + AI features (summarize, extend, translate, etc.)
│   ├── tags.py            # Tag and keyword management endpoints
│   ├── users.py           # User management
│   └── health.py          # Health check endpoint
├── models/                 # Data models
│   ├── note.py            # Note models (Note, NoteBase, NoteResponse)
│   ├── user.py            # User models (User, UserBase, UserResponse)
│   └── tag.py             # Tag and Keyword models with association tables
├── database/              # Database layer
│   ├── connection.py      # Database connection and session management
│   ├── note_crud.py       # CRUD operations for notes
│   ├── user_crud.py       # CRUD operations for users
│   ├── tag_crud.py        # CRUD operations for tags
│   └── keyword_crud.py    # CRUD operations for keywords
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
- `DELETE /notes/{id}` - Delete a note (requires authentication, ownership required)
- `GET /notes/public` - Get all public notes (no authentication required)

### AI Features (Notes)
- `GET /notes/{id}/summarize` - Generate AI summary of a note
- `GET /notes/{id}/extend` - Extend note content with AI insights
- `GET /notes/{id}/translate/{target_language}` - Translate note to target language
- `GET /notes/{id}/auto-tag` - Get AI-suggested tags and categories
- `GET /notes/{id}/keywords` - Extract keywords and main topics
- `GET /notes/{id}/sentiment` - Analyze emotional sentiment
- `GET /notes/{id}/related` - Find related notes

### Tags
- `GET /tags` - Get all tags for current user
- `POST /tags` - Create a new tag
- `DELETE /tags/{tag_id}` - Delete a tag
- `GET /notes/{note_id}/tags` - Get all tags for a note
- `POST /notes/{note_id}/tags/{tag_id}` - Add tag to note
- `DELETE /notes/{note_id}/tags/{tag_id}` - Remove tag from note

### Keywords
- `GET /keywords` - Get all keywords for current user
- `POST /keywords` - Create a new keyword
- `DELETE /keywords/{keyword_id}` - Delete a keyword
- `GET /notes/{note_id}/keywords` - Get all keywords for a note
- `POST /notes/{note_id}/keywords/{keyword_id}` - Add keyword to note
- `DELETE /notes/{note_id}/keywords/{keyword_id}` - Remove keyword from note

### Health
- `GET /health` - Health check endpoint

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Create a user**: `POST /user/create`
2. **Login to get token**: `POST /auth/login` with form data `username` and `password`
3. **Use the token**: Include `Authorization: Bearer <token>` header in protected requests

Tokens expire after 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`).

## AI Integration

JustNotes integrates with a local LLM API for AI-powered features:

- **Local LLM Server**: Runs on `http://localhost:1234/api/v1/chat`
- **Model**: Uses `google/gemma-3n-e4b` for all AI operations
- **Privacy**: All AI processing happens locally, no data sent to external services
- **Features**: Summarization, content extension, translation, auto-tagging, keyword extraction, sentiment analysis, and note relationship discovery

### Setting up the LLM Server

1. Install and run a local LLM server (e.g., LM Studio, Ollama)
2. Configure it to listen on `http://localhost:1234`
3. Load the `google/gemma-3n-e4b` model
4. AI features will automatically become available

## Security Features

- **Password Hashing** - Uses bcrypt for secure password storage
- **JWT Tokens** - Secure token-based authentication
- **Ownership Control** - Users can only modify their own notes, tags, and keywords
- **Public/Private Notes** - Granular access control for note visibility
- **Input Validation** - Pydantic models for request/response validation
- **User Isolation** - Tags and keywords are user-specific

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
- **Separation of concerns** - API, models, database, utils clearly separated
- **Dependency injection** - Database sessions and CRUD instances via FastAPI DI
- **Modular CRUD operations** - Separate files for each model (note_crud.py, user_crud.py, tag_crud.py, keyword_crud.py)
- **Type safety** - Comprehensive type hints and Pydantic validation
- **Clean architecture** - Modular components with clear responsibilities
- **Many-to-many relationships** - Tags and keywords linked to notes via association tables

## Docker Support

JustNotes includes full Docker support for easy deployment and development.

### Quick Start with Docker

1. **Clone and setup:**
```bash
git clone https://github.com/DatMayo/JustNotes.git
cd JustNotes
cp .env.example .env
# Edit .env with your settings
```

2. **Production deployment:**
```bash
docker-compose up -d
```

3. **Development with hot reload:**
```bash
docker-compose -f .docker/docker-compose.dev.yml up
```

### Docker Configuration

- **Dockerfile**: Multi-stage build with Python 3.11 slim
- **docker-compose.yml**: Production-ready with health checks
- **.docker/**: Separate development and production configurations
- **.dockerignore**: Optimized build context

### Environment Variables

All configuration is handled through environment variables with `JUSTNOTES_` prefix:

```bash
# Database
JUSTNOTES_DATABASE_URL=sqlite:///app/data/db.sqlite

# JWT Security
JUSTNOTES_SECRET_KEY=your-secret-key-change-in-production
JUSTNOTES_ALGORITHM=HS256
JUSTNOTES_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
JUSTNOTES_APP_NAME=JustNotes
JUSTNOTES_APP_VERSION=0.0.1
JUSTNOTES_APP_DESCRIPTION=JustNotes is a simple note-taking app

# Environment
JUSTNOTES_ENVIRONMENT=production
JUSTNOTES_DEBUG=false
JUSTNOTES_HOST=0.0.0.0
JUSTNOTES_PORT=8000
JUSTNOTES_RELOAD=false
```

### Docker Commands

```bash
# Build image
docker build -t justnotes .

# Run container
docker run -p 8000:8000 -v $(pwd)/data:/app/data justnotes

# Development with reload
docker-compose -f .docker/docker-compose.dev.yml up --build

# Production deployment
docker-compose -f .docker/docker-compose.prod.yml up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Data Persistence

- SQLite database stored in `./data/` directory
- Automatic volume mounting for data persistence
- Database survives container restarts

### Health Checks

- Built-in health check endpoint at `/health`
- Automatic container restart on failure
- Monitoring ready for production deployment

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.