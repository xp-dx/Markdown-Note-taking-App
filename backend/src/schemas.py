from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str


class NoteCreate(NoteBase):
    content: str


class NotePaths(NoteBase):
    md_note_path: str
    html_note_path: str
