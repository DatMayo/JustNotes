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


@router.get("/notes", tags=["Notes"], response_model=list[Note])
def get_notes(current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Get all notes for the current authenticated user.
    
    Args:
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        list[Note]: List of notes created by the current user
        
    Note:
        Only returns notes that belong to the authenticated user
    """
    return crud.get_user_notes(current_user.id)


@router.get("/notes/my", tags=["Notes"], response_model=list[Note])
def get_my_notes(current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Get all notes for the current user (both private and public).
    
    Args:
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        list[Note]: List of all notes created by the current user
        
    Note:
        Returns both private and public notes created by the user
    """
    return crud.get_user_notes(current_user.id)


@router.post("/notes/create", tags=["Notes"], response_model=NoteResponse, status_code=201)
def create_notes(item: NoteBase, current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Create a new note (requires authentication).
    
    Args:
        item: Note data from request body
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        NoteResponse: Created note with ID and timestamps
        
    Note:
        The createdBy field is automatically set to the current user's ID
    """
    # Set the createdBy to the current user's ID
    item.createdBy = current_user.id
    return crud.create_note(item)


@router.get("/notes/public", tags=["Notes"], response_model=list[Note])
def get_public_notes(crud: NoteCRUD = Depends(get_note_crud)):
    """
    Get all public notes (no authentication required).
    
    Args:
        crud: NoteCRUD instance for database operations
        
    Returns:
        list[Note]: List of all public notes
    """
    return crud.get_public_notes()


@router.get("/notes/{id}", tags=["Notes"], response_model=NoteResponse)
def get_note(id: int, current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Get a specific note by ID (requires authentication).
    
    Args:
        id: Note ID from URL path
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        NoteResponse: Note with specified ID
        
    Raises:
        HTTPException: 403 if user doesn't own the note and it's not public
        HTTPException: 404 if note is not found (from crud.get_note_by_id)
    """
    note = crud.get_note_by_id(id)
    # Check if user owns the note or it's public
    if note.createdBy != current_user.id and not note.isPublic:
        raise HTTPException(status_code=403, detail="Not authorized to access this note")
    return note


@router.put("/notes/{id}", tags=["Notes"], response_model=NoteResponse)
def update_note(id: int, item: NoteBase, current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    """
    Update a specific note by ID (requires authentication and ownership).
    
    Args:
        id: Note ID from URL path
        item: Updated note data from request body
        current_user: Authenticated user from JWT token
        crud: NoteCRUD instance for database operations
        
    Returns:
        NoteResponse: Updated note with new data
        
    Raises:
        HTTPException: 403 if user doesn't own the note
        HTTPException: 404 if note is not found (from crud.get_note_by_id)
        
    Note:
        The createdBy field is automatically set to prevent ownership changes
    """
    note = crud.get_note_by_id(id)
    # Check if user owns the note
    if note.createdBy != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this note")
    # Set the createdBy to the current user's ID to prevent ownership change
    item.createdBy = current_user.id
    return crud.update_note(id, item)
