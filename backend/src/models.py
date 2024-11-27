from sqlalchemy import Column, Integer, Text, String, Boolean

# from sqlalchemy_file import FileField

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)  # Название папки берем за заголовок
    md_note_path = Column(String(100), nullable=False)
    html_note_path = Column(String(100), nullable=False)
    # html_note = Column(String(100), nullable=False)
