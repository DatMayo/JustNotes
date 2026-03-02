from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings.
    
    Loads configuration from environment variables and .env file.
    Provides default values for all settings.
    
    Attributes:
        database_url: Database connection URL
        app_name: Name of the application
        app_version: Version of the application
        app_description: Description of the application
        secret_key: Secret key for JWT token signing
        algorithm: Algorithm used for JWT token signing
        access_token_expire_minutes: Minutes until JWT token expires
    """
    database_url: str = "sqlite:///db.sqlite"
    app_name: str = "JustNotes"
    app_version: str = "0.0.1"
    app_description: str = "JustNotes is a simple note-taking app"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        """
        Pydantic configuration for settings.
        
        Attributes:
            env_file: Path to environment file for loading variables
        """
        env_file = ".env"


# Global settings instance
settings = Settings()
