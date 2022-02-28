from __future__ import annotations

from pydantic import BaseModel


class Todo(BaseModel):
    tid: int
    name: str
    task: str
    complete: bool = False

    class Config:
        orm_mode = True


class TodoIn(BaseModel):
    name: str
    task: str

    class Config:
        orm_mode = True
