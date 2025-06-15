from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional
import shutil
import os

app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://search-debouncing-1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# In-memory store
notes = []
note_id = 1

@app.post("/notes/add")
def add_note(
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    global note_id
    image_url = None

    if image:
        filename = f"{note_id}_{image.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"https://search-debouncing.onrender.com/uploads/{filename}"

    note = {
        "id": note_id,
        "title": title,
        "content": content,
        "image_url": image_url
    }
    notes.append(note)
    note_id += 1
    return {"status": "Note added"}

@app.get("/notes/search")
def search_notes():
    return notes

@app.delete("/notes/delete/{note_id}")
def delete_note(note_id: int):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return {"status": "Note deleted"}

@app.put("/notes/update/{note_id}")
def update_note(note_id: int, title: str = Form(...), content: str = Form(...)):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["content"] = content
            return {"status": "Note updated"}
    return {"error": "Note not found"}
