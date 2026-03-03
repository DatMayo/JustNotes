from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

import requests

from ..models.user import UserResponse
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


def _check_note_access(note, current_user):
    """
    Helper function to check if user has access to a note.
    
    Args:
        note: Note object to check access for
        current_user: Current authenticated user
        
    Raises:
        HTTPException: 403 if user doesn't have access
    """
    if note.owner_id != current_user.id and not note.isPublic:
        raise HTTPException(status_code=403, detail="Not authorized to access this note")


def _call_llm_api(model: str, prompt: str) -> dict:
    """
    Helper function to call the local LLM API.
    
    Args:
        model: Model name to use
        prompt: System query/prompt for the model
        
    Returns:
        dict: JSON response from the LLM API
    """
    response = requests.post(
        "http://localhost:1234/api/v1/chat",
        headers={"Content-Type": "application/json"},
        json={"model": model, "input": prompt}
    )
    return response.json()


@router.get('/notes/{id}/summarize', tags=["Notes"])
def get_notes_summarize(id: int, current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    note, user = crud.get_note_by_id(id)
    _check_note_access(note, current_user)

    system_query = f'''You are an intelligent summarization assistant for a notes app.
Summarize the following article accurately and concisely, using the same language in which the article is written.
Focus on key ideas, relevant facts, and overall meaning — avoid unnecessary details or repetition.
Title: {note.title}
Article: {note.text}
Return only the summary text without commentary or formatting instructions.'''

    return _call_llm_api("andycurrent/llama-3-8b-lexi-uncensored@q4_k_m", system_query)

@router.get('/notes/{id}/extend', tags=["Notes"])
def get_notes_extend(id: int, current_user = Depends(get_current_user), crud: NoteCRUD = Depends(get_note_crud)):
    note, user = crud.get_note_by_id(id)
    _check_note_access(note, current_user)

    system_query = f'''You are an intelligent writing assistant for a notes app.
Extend the following article naturally in the same language it is written in.
Keep the original tone, style, and context consistent.
Add depth by expanding on key ideas, providing additional insights, examples, or relevant background information — but do not repeat what's already written.
Title: {note.title}
Article: {note.text}
Return only the extended version of the article.'''

    return _call_llm_api("andycurrent/llama-3-8b-lexi-uncensored@q4_k_m", system_query)

@router.get("/notes/{id}", tags=["Notes"], response_model=NoteResponse)
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
    note, user = crud.get_note_by_id(id)
    _check_note_access(note, current_user)
    
    owner: UserResponse = UserResponse(
        id=user.id,
        username=user.username,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt
    )
        
    response = NoteResponse(
        id=note.id,
        title=note.title,
        text=note.text,
        isPublic=note.isPublic,
        createdAt=note.createdAt,
        updatedAt=note.updatedAt,
        owner=owner
        )
    return response


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
