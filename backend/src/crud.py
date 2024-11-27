from sqlalchemy.orm import Session

import json

from . import models as _models, schemas as _schemas, services as _services


def get_all_notes(db: Session):
    notes = db.query(_models.Note.id, _models.Note.title).all()
    notes_json = []
    for note in notes:
        notes_json.append({"id": note[0], "title": note[1]})
    return json.loads(json.dumps(notes_json, default=str))


def get_note_by_id(db: Session, note_id: int):
    return db.query(_models.Note).filter(_models.Note.id == note_id).first()


# def create_note(db: Session, note: _schemas.NoteCreate):
#     db_note = _models.Note(title=note.title, note=note.content)
#     db.add(db_note)
#     db.commit()
#     db.refresh(db_note)
#     return db_note
def create_note_path(db: Session, note: _schemas.NotePaths):
    db_note = _models.Note(
        title=note.title,
        md_note_path=note.md_note_path,
        html_note_path=note.html_note_path,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
