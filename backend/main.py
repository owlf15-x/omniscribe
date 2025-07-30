
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware # Вот это добавляем!
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()
Base = declarative_base()

# Список разрешенных источников. В разработке можно поставить ["*"], но для продакшна - это пиздец.
origins = [
    "http://localhost:5173",  # Твой Svelte-сервер
    # "http://127.0.0.1:5173", # Иногда бывает и так
    # "https://your-domain.com", # Если в проде
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP-методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

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
    
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteCreate):
    with Session() as session:
        db_note = session.query(Note).filter(Note.id == note_id).first()
        if not db_note:
            # Как говорил Ницше, ошибки могут быть разными...
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        db_note.title = note.title
        db_note.content = note.content
        session.commit()
        session.refresh(db_note)
        return {"id": db_note.id, "title": db_note.title, "content": db_note.content}