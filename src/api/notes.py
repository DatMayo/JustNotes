from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database.connection import get_db_session
from ..database.crud import NoteCRUD
from ..models.note import Note, NoteBase, NoteResponse
from ..api.auth import get_current_user

# Router for note-related endpoints
router = APIRouter()


def get_note_crud(session: Session = Depends(get_db_session)):
    """
    Dependency function to get NoteCRUD instance with database session.
    
    Args:
        session: Database session from dependency injection
        
    Returns:
        NoteCRUD: Instance with database operations for notes
    """
    return NoteCRUD(session)


@router.get("/notes", tags=["Notes"], response_model=list[dict])
def get_notes(current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Get all notes for the current authenticated user.
    
    Args:
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        list[dict]: List of notes created by the current user with owner information
        
    Note:
        Only returns notes that belong to the authenticated user
    """
    return crud.get_user_notes(current_user.id)


@router.get("/notes/my", tags=["Notes"], response_model=list[dict])
def get_my_notes(current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Get all notes for the current user (both private and public).
    
    Args:
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        list[dict]: List of notes created by the current user with owner information
        
    Note:
        Returns both private and public notes created by the user
    """
    return crud.get_user_notes(current_user.id)


@router.post("/notes/create", tags=["Notes"], response_model=dict, status_code=201)
def create_notes(item: NoteBase, current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Create a new note (requires authentication).
    
    Args:
        item: Note data from request body
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        dict: Created note with ID, timestamps, and owner information
        
    Note:
        The note is automatically assigned to the current user
    """
    return crud.create_note(item, current_user.id)


@router.get("/notes/public", tags=["Notes"], response_model=list[dict])
def get_public_notes(crud: NoteCRUD = Depends(get_note_crud)):
    """
    Get all public notes (no authentication required).
    
    Args:
        crud: NoteCRUD instance for database operations
        
    Returns:
        list[dict]: List of all public notes with owner information
    """
    return crud.get_public_notes()


@router.get("/notes/{id}", tags=["Notes"], response_model=dict)
def get_note(id: int, current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Get a specific note by ID (requires authentication).
    
    Args:
        id: Note ID from URL path
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        dict: Note with specified ID and owner information
        
    Raises:
        HTTPException: 403 if user doesn't own the note and it's not public
        HTTPException: 404 if note is not found (from crud.get_note_by_id)
    """
    note = crud.get_note_by_id(id)
    # Check if user owns the note or it's public
    if note["owner_id"] != current_user.id and not note["isPublic"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this note")
    return note


@router.put("/notes/{id}", tags=["Notes"], response_model=dict)
def update_note(id: int, item: NoteBase, current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Update a specific note by ID (requires authentication and ownership).
    
    Args:
        id: Note ID from URL path
        item: Updated note data from request body
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        dict: Updated note with new data and owner information
        
    Raises:
        HTTPException: 403 if user doesn't own the note
        HTTPException: 404 if note is not found (from crud.get_note_by_id)
        
    Note:
        Ownership cannot be transferred through this endpoint
    """
    return crud.update_note(id, item, current_user.id)
