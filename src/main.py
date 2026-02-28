from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()

class Note(BaseModel):
    id: int
    title: str
    text: str
    isPublic: bool
    createdAt: int
    updatedAt: int

notes: list[Note] = [
    Note(
        id=1,
        title="Note 1",
        text="This is the first note",
        isPublic=True,
        createdAt=1629800000,
        updatedAt=1629800000
    ),
    Note(
        id=2,
        title="Note 2",
        text="This is the second note",
        isPublic=False,
        createdAt=1629800100,
        updatedAt=1629800100
    ),
    Note(
        id=3,
        title="Note 3",
        text="This is the third note",
        isPublic=True,
        createdAt=1629800200,
        updatedAt=1629800200
    ),
    Note(
        id=4,
        title="Note 4",
        text="This is the fourth note",
        isPublic=False,
        createdAt=1629800300,
        updatedAt=1629800300
    ),
    Note(
        id=5,
        title="Note 5",
        text="This is the fifth note",
        isPublic=True,
        createdAt=1629800400,
        updatedAt=1629800400
    ),
    Note(
        id=6,
        title="Note 6",
        text="This is the sixth note",
        isPublic=False,
        createdAt=1629800500,
        updatedAt=1629800500
    ),
    Note(
        id=7,
        title="Note 7",
        text="This is the seventh note",
        isPublic=True,
        createdAt=1629800600,
        updatedAt=1629800600
    ),
    Note(
        id=8,
        title="Note 8",
        text="This is the eighth note",
        isPublic=False,
        createdAt=1629800700,
        updatedAt=1629800700
    ),
    Note(
        id=9,
        title="Note 9",
        text="This is the ninth note",
        isPublic=True,
        createdAt=1629800800,
        updatedAt=1629800800
    ),
    Note(
        id=10,
        title="Note 10",
        text="This is the tenth note",
        isPublic=False,
        createdAt=1629800900,
        updatedAt=1629800900
    )
]

def get_current_time():
    return int(time.time())

@app.get("/notes", tags=["Notes"], response_model=list[Note])
def get_notes():
    return notes

@app.post("/notes/create", tags=["Notes"], response_model=Note, status_code=201)
def create_notes(item: Note):
    next_id = max(note.id for note in notes) + 1
    print(item)
    new_note = Note(
        id=next_id,
        title=item.title,
        text=item.text,
        isPublic=item.isPublic,
        createdAt=get_current_time(),
        updatedAt=get_current_time()
    )
    notes.append(new_note)
    return new_note

@app.get("/notes/public", tags=["Notes"], response_model=list[Note])
def get_public_notes():
    return [note for note in notes if note.isPublic]

@app.get("/notes/{id}", tags=["Notes"], response_model=Note)
def get_note(id: int):
    try:
        note_id = int(id)
        note = next((note for note in notes if note.id == note_id), None)
        if note is None:
            return {"error": "Could not find note"}
        return note
    except ValueError:
        return {"error": "Could not find note"}
@app.get("/health", status_code=200, tags=["Health"])
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)