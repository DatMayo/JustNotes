from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.note import Note
from ..models.user import User
from ..models.tag import Tag, Keyword, NoteTagLink, NoteKeywordLink


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
                "owner_id": note.owner_id,
            }

            # Add owner information
            if note.owner_id:
                user = self.session.exec(
                    select(User).where(User.id == note.owner_id)
                ).one_or_none()
                if user:
                    note_dict["owner"] = {
                        "id": user.id,
                        "username": user.username,
                        "createdAt": user.createdAt,
                        "updatedAt": user.updatedAt,
                    }

            result.append(note_dict)

        return result

    def get_public_notes(self):
        """
        Retrieve all public notes from the database with owner information.

        Returns:
            list[dict]: List of public notes with owner information as dictionaries
        """
        notes = self.session.exec(select(Note).where(Note.isPublic)).all()

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
                "owner_id": note.owner_id,
            }

            # Add owner information
            if note.owner_id:
                user = self.session.exec(
                    select(User).where(User.id == note.owner_id)
                ).one_or_none()
                if user:
                    note_dict["owner"] = {
                        "id": user.id,
                        "username": user.username,
                        "createdAt": user.createdAt,
                        "updatedAt": user.updatedAt,
                    }

            result.append(note_dict)

        return result

    def get_note_by_id(self, note_id: int):
        """
        Retrieve a specific note by ID with user information.

        Args:
            note_id: ID of the note to retrieve

        Returns:
            tuple: (Note, User) objects

        Raises:
            HTTPException: 404 if note is not found
        """
        # Execute a SQL query to select a note by ID with user join
        statement = select(Note, User).join(User).where(Note.id == note_id)
        result = self.session.exec(statement).one_or_none()

        if result is None:
            raise HTTPException(status_code=404, detail="Note not found")

        note, user = result
        return note, user

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
        result = self.session.exec(
            select(Note).where(
                (Note.title == note_data.title) & (Note.owner_id == user_id)
            )
        ).one_or_none()
        if result is not None:
            # Raise an exception if a note with the same title already exists
            raise HTTPException(
                status_code=400, detail="Note with same title already exists"
            )

        # Create a new note
        new_note = Note(
            title=note_data.title,
            text=note_data.text,
            owner_id=user_id,  # Use owner_id instead of createdBy
            isPublic=note_data.isPublic,
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
            "owner_id": new_note.owner_id,
        }

        # Add owner information
        user = self.session.exec(select(User).where(User.id == user_id)).one_or_none()
        if user:
            note_dict["owner"] = {
                "id": user.id,
                "username": user.username,
                "createdAt": user.createdAt,
                "updatedAt": user.updatedAt,
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
            dict: Updated note with owner information

        Raises:
            HTTPException: 404 if note is not found
            HTTPException: 403 if user doesn't own the note
        """
        # Retrieve the note by ID
        note, user = self.get_note_by_id(note_id)

        # Check if user owns the note
        if note.owner_id != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to modify this note"
            )

        # Update the note's data
        note.title = note_data.title
        note.text = note_data.text
        note.isPublic = note_data.isPublic
        note.updatedAt = int(__import__("time").time())
        # owner_id remains unchanged to prevent ownership transfer

        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)

        # Convert to dictionary with owner information
        note_dict = {
            "id": note.id,
            "title": note.title,
            "text": note.text,
            "isPublic": note.isPublic,
            "createdAt": note.createdAt,
            "updatedAt": note.updatedAt,
            "owner_id": note.owner_id,
        }

        # Add owner information
        note_dict["owner"] = {
            "id": user.id,
            "username": user.username,
            "createdAt": user.createdAt,
            "updatedAt": user.updatedAt,
        }

        return note_dict

    def delete_note(self, note_id: int, user_id: int):
        """
        Delete a note from the database.

        Args:
            note_id: ID of the note to delete
            user_id: ID of the user attempting to delete

        Returns:
            dict: Success message

        Raises:
            HTTPException: 404 if note is not found
            HTTPException: 403 if user doesn't own the note
        """
        # Retrieve the note by ID
        note, user = self.get_note_by_id(note_id)

        # Check if user owns the note
        if note.owner_id != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this note"
            )

        # Delete the note
        self.session.delete(note)
        self.session.commit()

        return {"message": "Note deleted successfully"}


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
        return self.session.exec(
            select(User).where(User.username == username)
        ).one_or_none()

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
        result = self.session.exec(
            select(User).where(User.username == user_data.username)
        ).one_or_none()
        if result is not None:
            # Raise an exception if the user already exists
            raise HTTPException(status_code=400, detail="User already exists")

        # Create a new user
        new_user = User(username=user_data.username, password=user_data.password)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user


class TagCRUD:
    """
    CRUD operations for Tag model.

    Provides database operations for creating, reading, and managing tags.
    All operations are performed within a database session.
    """

    def __init__(self, session: Session):
        """
        Initialize TagCRUD with database session.

        Args:
            session: SQLModel Session for database operations
        """
        self.session = session

    def get_or_create_tag(self, name: str, category: str | None, owner_id: int):
        """
        Get existing tag or create new one if it doesn't exist.

        Args:
            name: Tag name
            category: Optional category
            owner_id: User ID who owns this tag

        Returns:
            Tag: Existing or newly created tag
        """
        tag = self.session.exec(
            select(Tag).where((Tag.name == name) & (Tag.owner_id == owner_id))
        ).one_or_none()

        if tag is None:
            tag = Tag(name=name, category=category, owner_id=owner_id)
            self.session.add(tag)
            self.session.commit()
            self.session.refresh(tag)

        return tag

    def get_user_tags(self, owner_id: int):
        """
        Get all tags for a specific user.

        Args:
            owner_id: User ID

        Returns:
            list[Tag]: List of tags owned by the user
        """
        return self.session.exec(select(Tag).where(Tag.owner_id == owner_id)).all()

    def add_tag_to_note(self, note_id: int, tag_id: int):
        """
        Link a tag to a note.

        Args:
            note_id: Note ID
            tag_id: Tag ID
        """
        existing = self.session.exec(
            select(NoteTagLink).where(
                (NoteTagLink.note_id == note_id) & (NoteTagLink.tag_id == tag_id)
            )
        ).one_or_none()

        if existing is None:
            link = NoteTagLink(note_id=note_id, tag_id=tag_id)
            self.session.add(link)
            self.session.commit()

    def remove_tag_from_note(self, note_id: int, tag_id: int):
        """
        Remove a tag from a note.

        Args:
            note_id: Note ID
            tag_id: Tag ID
        """
        link = self.session.exec(
            select(NoteTagLink).where(
                (NoteTagLink.note_id == note_id) & (NoteTagLink.tag_id == tag_id)
            )
        ).one_or_none()

        if link:
            self.session.delete(link)
            self.session.commit()

    def get_note_tags(self, note_id: int):
        """
        Get all tags for a specific note.

        Args:
            note_id: Note ID

        Returns:
            list[Tag]: List of tags associated with the note
        """
        statement = select(Tag).join(NoteTagLink).where(NoteTagLink.note_id == note_id)
        return self.session.exec(statement).all()

    def delete_tag(self, tag_id: int, owner_id: int):
        """
        Delete a tag (only if owned by user).

        Args:
            tag_id: Tag ID
            owner_id: User ID

        Raises:
            HTTPException: 404 if tag not found or 403 if not owned by user
        """
        tag = self.session.exec(select(Tag).where(Tag.id == tag_id)).one_or_none()

        if tag is None:
            raise HTTPException(status_code=404, detail="Tag not found")

        if tag.owner_id != owner_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this tag"
            )

        self.session.delete(tag)
        self.session.commit()


class KeywordCRUD:
    """
    CRUD operations for Keyword model.

    Provides database operations for creating, reading, and managing keywords.
    All operations are performed within a database session.
    """

    def __init__(self, session: Session):
        """
        Initialize KeywordCRUD with database session.

        Args:
            session: SQLModel Session for database operations
        """
        self.session = session

    def get_or_create_keyword(self, term: str, is_main_topic: bool, owner_id: int):
        """
        Get existing keyword or create new one if it doesn't exist.

        Args:
            term: Keyword term
            is_main_topic: Whether this is a main topic
            owner_id: User ID who owns this keyword

        Returns:
            Keyword: Existing or newly created keyword
        """
        keyword = self.session.exec(
            select(Keyword).where(
                (Keyword.term == term) & (Keyword.owner_id == owner_id)
            )
        ).one_or_none()

        if keyword is None:
            keyword = Keyword(term=term, is_main_topic=is_main_topic, owner_id=owner_id)
            self.session.add(keyword)
            self.session.commit()
            self.session.refresh(keyword)

        return keyword

    def get_user_keywords(self, owner_id: int):
        """
        Get all keywords for a specific user.

        Args:
            owner_id: User ID

        Returns:
            list[Keyword]: List of keywords owned by the user
        """
        return self.session.exec(
            select(Keyword).where(Keyword.owner_id == owner_id)
        ).all()

    def add_keyword_to_note(self, note_id: int, keyword_id: int):
        """
        Link a keyword to a note.

        Args:
            note_id: Note ID
            keyword_id: Keyword ID
        """
        existing = self.session.exec(
            select(NoteKeywordLink).where(
                (NoteKeywordLink.note_id == note_id)
                & (NoteKeywordLink.keyword_id == keyword_id)
            )
        ).one_or_none()

        if existing is None:
            link = NoteKeywordLink(note_id=note_id, keyword_id=keyword_id)
            self.session.add(link)
            self.session.commit()

    def remove_keyword_from_note(self, note_id: int, keyword_id: int):
        """
        Remove a keyword from a note.

        Args:
            note_id: Note ID
            keyword_id: Keyword ID
        """
        link = self.session.exec(
            select(NoteKeywordLink).where(
                (NoteKeywordLink.note_id == note_id)
                & (NoteKeywordLink.keyword_id == keyword_id)
            )
        ).one_or_none()

        if link:
            self.session.delete(link)
            self.session.commit()

    def get_note_keywords(self, note_id: int):
        """
        Get all keywords for a specific note.

        Args:
            note_id: Note ID

        Returns:
            list[Keyword]: List of keywords associated with the note
        """
        statement = (
            select(Keyword)
            .join(NoteKeywordLink)
            .where(NoteKeywordLink.note_id == note_id)
        )
        return self.session.exec(statement).all()

    def delete_keyword(self, keyword_id: int, owner_id: int):
        """
        Delete a keyword (only if owned by user).

        Args:
            keyword_id: Keyword ID
            owner_id: User ID

        Raises:
            HTTPException: 404 if keyword not found or 403 if not owned by user
        """
        keyword = self.session.exec(
            select(Keyword).where(Keyword.id == keyword_id)
        ).one_or_none()

        if keyword is None:
            raise HTTPException(status_code=404, detail="Keyword not found")

        if keyword.owner_id != owner_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this keyword"
            )

        self.session.delete(keyword)
        self.session.commit()
