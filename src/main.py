from fastapi import FastAPI
from .database import create_db_and_tables
from .api import notes_router, users_router, health_router, auth_router
from .config import settings

# Create FastAPI application instance with configuration
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "JustNotes",
        "url": "https://github.com/DatMayo/JustNotes/",
        "email": "mario.franze@gmail.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/DatMayo/JustNotes/blob/main/LICENSE"
    }
)

# Create database tables on application startup
create_db_and_tables()

# Include API routers
# Order matters: auth router should be included first for authentication endpoints
app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(users_router)
app.include_router(health_router)

# Run the application when this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)