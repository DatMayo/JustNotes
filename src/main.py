from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
import time
import bcrypt

def get_current_time() -> int:
    return int(time.time())

class NoteBase(BaseModel):
    title: str
    text: str
    createdBy: int
    isPublic: bool

class Note(NoteBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    createdAt: int = Field(default_factory=get_current_time)
    updatedAt: int = Field(default_factory=get_current_time)

class NoteResponse(NoteBase):
    id: int
    createdAt: int
    updatedAt: int

class UserBase(BaseModel):
    username: str
    password: str

class User(UserBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    createdAt: int = Field(default_factory=get_current_time)
    updatedAt: int = Field(default_factory=get_current_time)

class UserResponse(BaseModel):
    id: int
    username: str
    createdAt: int
    updatedAt: int

app = FastAPI(
    title="JustNotes",
    description="JustNotes is a simple note-taking app",
    version="0.0.1",
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

engine = create_engine("sqlite:///db.sqlite")
SQLModel.metadata.create_all(engine)

@app.get("/notes", tags=["Notes"], response_model=list[Note])
def get_notes():
    with Session(engine) as session:
        return session.exec(select(Note)).all()

@app.post("/notes/create", tags=["Notes"], response_model=NoteResponse, status_code=201)
def create_notes(item: NoteBase):
    with Session(engine) as session:

        # Check if user exists
        result = session.exec(select(User).where(User.id == item.createdBy)).one_or_none()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if note with same title exists
        result = session.exec(select(Note).where(Note.title == item.title)).one_or_none()
        if result is not None:
            raise HTTPException(status_code=400, detail="Note with same title already exists")            
        new_note = Note(title=item.title, text=item.text, createdBy=item.createdBy, isPublic=item.isPublic)
        session.add(new_note)
        session.commit()
        session.refresh(new_note)
        return new_note
        

@app.get("/notes/public", tags=["Notes"], response_model=list[Note])
def get_public_notes():
    with Session(engine) as session:
        return session.exec(select(Note).where(Note.isPublic == True)).all()

@app.get("/notes/{id}", tags=["Notes"], response_model=NoteResponse)
def get_note(id: int):
    with Session(engine) as session:
        note = session.exec(select(Note).where(Note.id == id)).one_or_none()
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return note

@app.put("/notes/{id}", tags=["Notes"], response_model=NoteResponse)
def update_note(id: int, item: NoteBase):
    with Session(engine) as session:
        note = session.exec(select(Note).where(Note.id == id)).one_or_none()
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        note.title = item.title
        note.text = item.text
        note.createdBy = item.createdBy
        note.isPublic = item.isPublic
        session.commit()
        session.refresh(note)
        return note

@app.post("/user/create", tags=["User"], response_model=UserResponse)
async def create_user(user: UserBase):
    with Session(engine) as session:
        # Check if user exists
        result = session.exec(select(User).where(User.username == user.username)).one_or_none()
        if result is not None:
            # ToDo: Better error handling
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Hash password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        new_user = User(username=user.username, password=hashed_password)
        session.add(new_user)
        session.commit()

        session.refresh(new_user)
        return new_user
        

@app.get("/user/list", tags=["User"], response_model=list[UserResponse])
def list_users():
    with Session(engine) as session:
        return session.exec(select(User)).all()

@app.get("/health", status_code=200, tags=["Health"])
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)