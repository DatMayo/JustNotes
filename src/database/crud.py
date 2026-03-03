from sqlalchemy.orm import session
from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.note import Note
from ..models.user import User
import bcrypt

class NoteCRUD:
    """
    CRUD operations for Note model.
    
    Provides database operations for creating, reading, and updating notes.
    All operations are performed within a database session.
    """
    
    def __init__(self, session: Session):
        """
        Initialize NoteCRUD with database session.
        
        Args:
            session: SQLModel Session for database operations
        """
        self.session = session
    
    def get_all_notes(self):
        """
        Retrieve all notes from the database (admin function).
        
        Returns:
            list[Note]: List of all notes in the database
        """
        # Execute a SQL query to select all notes from the database
        return self.session.exec(select(Note)).all()
    
    def get_user_notes(self, user_id: int):
        """
        Retrieve all notes created by a specific user with owner information.
        
        Args:
            user_id: ID of the user whose notes to retrieve
            
        Returns:
            list[dict]: List of notes with owner information as dictionaries
        """
        notes = self.session.exec(select(Note).where(Note.owner_id == user_id)).all()
        
        # Convert to dictionaries with owner information
        result = []
        for note in notes:
            note_dict = {
                "id": note.id,
                "title": note.title,
                "text": note.text,
                "isPublic": note.isPublic,
                "createdAt": note.createdAt,
                "updatedAt": note.updatedAt,
                "owner_id": note.owner_id
            }
            
            # Add owner information
            if note.owner_id:
                user = self.session.exec(select(User).where(User.id == note.owner_id)).one_or_none()
                if user:
                    note_dict["owner"] = {
                        "id": user.id,
                        "username": user.username,
                        "createdAt": user.createdAt,
                        "updatedAt": user.updatedAt
                    }
            
            result.append(note_dict)
        
        return result
    
    def get_public_notes(self):
        """
        Retrieve all public notes from the database with owner information.
        
        Returns:
            list[dict]: List of public notes with owner information as dictionaries
        """
        notes = self.session.exec(select(Note).where(Note.isPublic == True)).all()
        
        # Convert to dictionaries with owner information
        result = []
        for note in notes:
            note_dict = {
                "id": note.id,
                "title": note.title,
                "text": note.text,
                "isPublic": note.isPublic,
                "createdAt": note.createdAt,
                "updatedAt": note.updatedAt,
                "owner_id": note.owner_id
            }
            
            # Add owner information
            if note.owner_id:
                user = self.session.exec(select(User).where(User.id == note.owner_id)).one_or_none()
                if user:
                    note_dict["owner"] = {
                        "id": user.id,
                        "username": user.username,
                        "createdAt": user.createdAt,
                        "updatedAt": user.updatedAt
                    }
            
            result.append(note_dict)
        
        return result
    
    def get_note_by_id(self, note_id: int):
        """
        Retrieve a specific note by ID with user information.
        
        Args:
            note_id: ID of the note to retrieve
            
        Returns:
            dict: Note with specified ID and owner information
            
        Raises:
            HTTPException: 404 if note is not found
        """
        # Execute a SQL query to select a note by ID
        statement = select(Note, User).join(User).where(Note.id == note_id)
        results = self.session.exec(statement)
        note = results.one()

        return note
        '''
        note = self.session.exec(select(Note).where(Note.id == note_id)).one_or_none()
        if note is None:
            # Raise an exception if the note is not found
            raise HTTPException(status_code=404, detail="Note not found")

        print(note)
        
        # Convert to dictionary with owner information
        note_dict = {
            "id": note.id,
            "title": note.title,
            "text": note.text,
            "isPublic": note.isPublic,
            "createdAt": note.createdAt,
            "updatedAt": note.updatedAt,
            "owner_id": note.owner_id
        }
        
        # Add owner information
        if note.owner_id:
            user = self.session.exec(select(User).where(User.id == note.owner_id)).one_or_none()
            if user:
                note_dict["owner"] = {
                    "id": user.id,
                    "username": user.username,
                    "createdAt": user.createdAt,
                    "updatedAt": user.updatedAt
                }
        
        return note_dict
        '''
    
    def create_note(self, note_data, user_id: int):
        """
        Create a new note in the database.
        
        Args:
            note_data: NoteBase object with note data
            user_id: ID of the user creating the note
            
        Returns:
            Note: Created note with ID and timestamps
            
        Raises:
            HTTPException: 404 if user doesn't exist
            HTTPException: 400 if note with same title already exists
        """
        # Check if user exists
        result = self.session.exec(select(User).where(User.id == user_id)).one_or_none()
        if result is None:
            # Raise an exception if the user is not found
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if note with same title exists for this user
        result = self.session.exec(select(Note).where(
            (Note.title == note_data.title) & (Note.owner_id == user_id)
        )).one_or_none()
        if result is not None:
            # Raise an exception if a note with the same title already exists
            raise HTTPException(status_code=400, detail="Note with same title already exists")
        
        # Create a new note
        new_note = Note(
            title=note_data.title, 
            text=note_data.text, 
            owner_id=user_id,  # Use owner_id instead of createdBy
            isPublic=note_data.isPublic
        )
        self.session.add(new_note)
        self.session.commit()
        self.session.refresh(new_note)
        
        # Convert to dictionary with owner information
        note_dict = {
            "id": new_note.id,
            "title": new_note.title,
            "text": new_note.text,
            "isPublic": new_note.isPublic,
            "createdAt": new_note.createdAt,
            "updatedAt": new_note.updatedAt,
            "owner_id": new_note.owner_id
        }
        
        # Add owner information
        user = self.session.exec(select(User).where(User.id == user_id)).one_or_none()
        if user:
            note_dict["owner"] = {
                "id": user.id,
                "username": user.username,
                "createdAt": user.createdAt,
                "updatedAt": user.updatedAt
            }
        
        return note_dict
    
    def update_note(self, note_id: int, note_data, user_id: int):
        """
        Update an existing note in the database.
        
        Args:
            note_id: ID of the note to update
            note_data: NoteBase object with updated note data
            user_id: ID of the user attempting to update
            
        Returns:
            Note: Updated note with new data
            
        Raises:
            HTTPException: 404 if note is not found
            HTTPException: 403 if user doesn't own the note
        """
        # Retrieve the note by ID
        note = self.get_note_by_id(note_id)
        
        print(note)
        # Check if user owns the note
        if note['owner_id'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this note")
        
        # Update the note's data
        note['title'] = note_data.title
        note['text'] = note_data.text
        note['isPublic'] = note_data.isPublic
        # owner_id remains unchanged to prevent ownership transfer
        
        self.session.commit()
        '''
        self.session.refresh(note)
        
        # Convert to dictionary with owner information
        note_dict = {
            "id": note.id,
            "title": note.title,
            "text": note.text,
            "isPublic": note.isPublic,
            "createdAt": note.createdAt,
            "updatedAt": note.updatedAt,
            "owner_id": note.owner_id
        }
        
        # Add owner information
        user = self.session.exec(select(User).where(User.id == note.owner_id)).one_or_none()
        if user:
            note_dict["owner"] = {
                "id": user.id,
                "username": user.username,
                "createdAt": user.createdAt,
                "updatedAt": user.updatedAt
            }
        '''
        return {}


class UserCRUD:
    """
    CRUD operations for User model.
    
    Provides database operations for creating and reading users.
    All operations are performed within a database session.
    """
    
    def __init__(self, session: Session):
        """
        Initialize UserCRUD with database session.
        
        Args:
            session: SQLModel Session for database operations
        """
        self.session = session
    
    def get_all_users(self):
        """
        Retrieve all users from the database.
        
        Returns:
            list[User]: List of all users in the database
        """
        # Execute a SQL query to select all users from the database
        return self.session.exec(select(User)).all()

    def get_user_by_id(self, user_id: int):
        """
        Retrieve a specific user by ID.
        
        Args:
            user_id: ID of the user to retrieve
            
        Returns:
            User: User with specified ID, or None if not found
        """
        # Execute a SQL query to select a user by ID
        return self.session.exec(select(User).where(User.id == user_id)).one_or_none()

    def get_user_by_username(self, username: str):
        """
        Retrieve a specific user by username.
        
        Args:
            username: Username of the user to retrieve
            
        Returns:
            User: User with specified username, or None if not found
        """
        # Execute a SQL query to select a user by username
        return self.session.exec(select(User).where(User.username == username)).one_or_none()
    
    def create_user(self, user_data):
        """
        Create a new user in the database.
        
        Args:
            user_data: UserBase object with user data (password should be pre-hashed)
            
        Returns:
            User: Created user with ID and timestamps
            
        Raises:
            HTTPException: 400 if user with same username already exists
            
        Note:
            Password should be hashed before calling this method
        """
        # Check if user exists
        result = self.session.exec(select(User).where(User.username == user_data.username)).one_or_none()
        if result is not None:
            # Raise an exception if the user already exists
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create a new user
        new_user = User(username=user_data.username, password=user_data.password)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
