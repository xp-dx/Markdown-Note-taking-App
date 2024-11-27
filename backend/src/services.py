import markdown

import pathlib

from spellchecker import SpellChecker

from . import database as _database, models as _models


def create_database():
    return _models.Base.metadata.create_all(_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def unic_dir(path: pathlib.Path):
    path = pathlib.Path(str(path) + " (1)")
    while path.exists():
        str_path = str(path)
        rindex_open_parenthesis = str_path.rindex("(")
        path = pathlib.Path(
            str_path[:rindex_open_parenthesis]
            + "("
            + str(int(str_path[rindex_open_parenthesis + 1 : -1]) + 1)
            + ")"
        )
    return path


def create_directory(path: pathlib.Path):
    if not path.exists():
        path.mkdir()
    else:
        path = unic_dir(path)
        path.mkdir()
    return str(path)


def create_md_file(path, title, content):
    with open(f"{path}{title}.md", "w") as md_file:
        md_file.write(content)


def create_html_file(path, markdown_note, html_note):
    with open(f"{path}{markdown_note}", "r") as markdown_file:
        with open(f"{path}{html_note}", "w") as html_file:
            html_file.write(markdown.markdown(markdown_file.read()))


def check_grammar(text: str):
    spell = SpellChecker()
    misspelled = spell.unknown(text.split())
    return misspelled
