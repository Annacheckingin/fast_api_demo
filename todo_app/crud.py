from typing import List, Optional
from sqlmodel import Session, select
from db import engine
from .models import Todo as TodoModel
from .schemas import TodoCreate


def list_todos() -> List[TodoModel]:
    with Session(engine) as session:
        return session.exec(select(TodoModel)).all()


def create_todo(data: TodoCreate) -> TodoModel:
    todo = TodoModel(title=data.title, description=data.description)
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


def get_todo(todo_id: int) -> Optional[TodoModel]:
    with Session(engine) as session:
        return session.get(TodoModel, todo_id)


def update_todo(todo_id: int, data: TodoCreate) -> Optional[TodoModel]:
    with Session(engine) as session:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return None
        todo.title = data.title
        todo.description = data.description
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


def toggle_todo(todo_id: int) -> Optional[TodoModel]:
    with Session(engine) as session:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return None
        todo.done = not todo.done
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


def delete_todo(todo_id: int) -> bool:
    with Session(engine) as session:
        todo = session.get(TodoModel, todo_id)
        if not todo:
            return False
        session.delete(todo)
        session.commit()
        return True
