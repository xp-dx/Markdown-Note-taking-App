from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from typing import Annotated

import pathlib

from . import services as _services, crud as _crud, schemas as _schemas

app = FastAPI(title="Markdown Note-taking App", version="0.0.1")
app.mount("/static", StaticFiles(directory="./static"), name="static")
# app.mount("/data", StaticFiles(directory="./data/english (1)"), name="data")

_services.create_database()

templates = Jinja2Templates(directory="templates")


@app.get("/check-grammar")
def check_grammar(text: str):
    return {"message": "Hello World"}


@app.get("/write-note", response_class=HTMLResponse)
async def write_note(request: Request):
    referer = request.headers.get("Referer")
    if referer:
        return templates.TemplateResponse(
            "write-note.html", {"request": request, "referer": referer}
        )
    return templates.TemplateResponse("write-note.html", {"request": request})


@app.post("/write-note", response_model=_schemas.NotePaths)
async def write_note(
    new_note: Annotated[_schemas.NoteCreate, Form()],
    db: Session = Depends(_services.get_db),
):
    dir_path = "./data/" + new_note.title
    md_note_name = f"{new_note.title}.md"
    html_note_name = f"{new_note.title}.html"
    note_dir = _services.create_directory(pathlib.Path(dir_path))
    dir_path = "./" + note_dir + "/"
    _services.create_md_file(
        path=dir_path, title=new_note.title, content=new_note.content
    )
    _services.create_html_file(
        path=dir_path,
        markdown_note=md_note_name,
        html_note=html_note_name,
    )

    return _crud.create_note_path(
        db,
        _schemas.NotePaths(
            title=note_dir.replace("data/", "", 1),
            md_note_path=dir_path + md_note_name,
            html_note_path=dir_path + html_note_name,
        ),
    )


@app.post("/upload-img")
async def upload_img():
    return


@app.get("/upload-note", response_class=HTMLResponse)
async def write_note(request: Request):
    return templates.TemplateResponse("upload-note.html", {"request": request})


@app.post("/upload-note")
def upload_note(
    # markdown_note,
    # db: Session = Depends(_services.get_db()),
):
    # _services.create_html_file(
    #     markdown_note,
    #     markdown_note[: markdown_note.index(".")] + ".html",
    # )
    return {"message": "Hello World"}


@app.get("/home", response_class=HTMLResponse)
def all_notes(request: Request, db: Session = Depends(_services.get_db)):
    notes = _crud.get_all_notes(db)
    return templates.TemplateResponse("home.html", {"request": request, "notes": notes})


from starlette.routing import Mount
from datetime import datetime


@app.get(
    "/note/{note_id}",  # response_class=HTMLResponse
)
def html_markdown(
    request: Request, note_id: int, db: Session = Depends(_services.get_db)
):
    note_db = _crud.get_note_by_id(db, note_id)
    # for index, route in enumerate(app.routes):
    #     if isinstance(route, Mount) and route.path == "":
    #         del app.routes[index]
    #         break
    app.mount("/", StaticFiles(directory=f"./data/{note_db.title}"), name="data")
    # templates2 = Jinja2Templates(directory=f"data/{note_db.title}")

    # res = dict()
    # for route in app.routes:
    #     if isinstance(route, Mount):
    #         res.setdefault(route.path, route.name)
    # return res
    # img_path = StaticFiles(directory=f"./data/{note_db.title}/img")
    # return img_path.directory
    with open(note_db.html_note_path, "r") as html_file:
        note = (
            html_file.read()
            .replace("<code>", "<pre><code>")
            .replace("</code>", "</code></pre>")
        )
        # .replace(
        #     'src="/kitten_rage.jpg',
        #     "src=\"{{ url_for('static', path='/img/ABSOLUTE2.gif') }}\"",
        # )
    return templates.TemplateResponse(
        "note.html", {"request": request, "note": note, "note_db": note_db}
    )
