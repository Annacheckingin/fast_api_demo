from pydantic import BaseModel
from typing import Optional


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class Todo(TodoCreate):
    id: int

    class Config:
        orm_mode = True
