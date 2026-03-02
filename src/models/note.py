from pydantic import BaseModel
from sqlmodel import Field, SQLModel
import time


def get_current_time() -> int:
    """
    Get current Unix timestamp.
    
    Returns:
        int: Current Unix timestamp in seconds
    """
    return int(time.time())


class NoteBase(BaseModel):
    """
    Base model for note data (without database fields).
    
    Attributes:
        title: Title of the note
        text: Content/body of the note
        createdBy: ID of the user who created the note
        isPublic: Whether the note is publicly accessible
    """
    title: str
    text: str
    createdBy: int
    isPublic: bool


class Note(NoteBase, SQLModel, table=True):
    """
    Complete note model with database fields.
    
    Inherits from NoteBase and adds database-specific fields.
    Represents the notes table in the database.
    
    Attributes:
        id: Primary key (auto-generated)
        createdAt: Unix timestamp when note was created
        updatedAt: Unix timestamp when note was last updated
    """
    id: int | None = Field(default=None, primary_key=True)
    createdAt: int = Field(default_factory=get_current_time)
    updatedAt: int = Field(default_factory=get_current_time)


class NoteResponse(NoteBase):
    """
    Response model for note data (includes database fields).
    
    Used for API responses to include all note information
    including timestamps and ID.
    
    Attributes:
        id: Note ID
        createdAt: Creation timestamp
        updatedAt: Last update timestamp
    """
    id: int
    createdAt: int
    updatedAt: int
