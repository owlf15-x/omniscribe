from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)

engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class NoteCreate(BaseModel):
    title: str
    content: str

@app.get("/notes")
def get_notes():
    with Session() as session:
        notes = session.query(Note).all()
        return [{"id": note.id, "title": note.title, "content": note.content} for note in notes]

@app.post("/notes")
def create_note(note: NoteCreate):
    with Session() as session:
        new_note = Note(title=note.title, content=note.content)
        session.add(new_note)
        session.commit()
        return {"id": new_note.id, "title": new_note.title, "content": new_note.content}

@app.on_event("startup")
def startup_event():
    with Session() as session:
        if not session.query(Note).first():
            session.add(Note(title="Sample Note", content="# Hello, OmniScribe!\nThis is a test."))
            session.commit()