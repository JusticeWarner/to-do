from __future__ import annotations

import uvicorn  # type: ignore
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from todo import models, schemas

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))


@app.get("/")
async def index() -> Response:
    """Returns the index page."""
    return FileResponse("static/index.html")


@app.get("/todos", response_model=list[schemas.Todo])
async def get_todos() -> list[schemas.Todo]:
    """Gets a list of all current to-do's."""
    return [schemas.Todo.from_orm(model) for model in await models.Todo.all()]


@app.post("/todos", response_model=schemas.Todo)
async def add_todo(todo: schemas.TodoIn) -> schemas.Todo:
    """Adds a new to-do."""
    obj = await models.Todo.create(**todo.dict())

    await obj.save()
    return schemas.Todo.from_orm(obj)


@app.delete("/todos/{tid}", response_model=schemas.Todo)
async def del_todo_by_id(tid: int) -> schemas.Todo:
    """Deletes a to-do by id."""
    obj = await models.Todo.get(tid=tid)

    if not obj:
        raise HTTPException(404, f"No object found with todo ID {tid}")

    await obj.delete()
    return schemas.Todo.from_orm(obj)


@app.delete("/todos", response_model=schemas.Todo)
async def del_todo_by_name(name: str) -> schemas.Todo:
    """Deletes a to-do by name."""
    obj = await models.Todo.get(name=name)

    if not obj:
        raise HTTPException(404, f"No object found with name {name}")

    await obj.delete()
    return schemas.Todo.from_orm(obj)


if __name__ == "__main__":
    load_dotenv()

    register_tortoise(
        app,
        db_url="sqlite://todo/data/database.db",
        modules={"models": ["todo.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    uvicorn.run(app, host="0.0.0.0", port=80)  # type: ignore
