from fastapi import APIRouter, HTTPException
from typing import List
from . import crud, schemas

router = APIRouter()


@router.post("/todos", response_model=schemas.Todo, status_code=201)
def create_todo(payload: schemas.TodoCreate):
    return crud.create_todo(payload)


@router.get("/todos", response_model=List[schemas.Todo])
def list_todos():
    return crud.list_todos()


@router.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_todo(todo_id: int):
    todo = crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, payload: schemas.TodoCreate):
    todo = crud.update_todo(todo_id, payload)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.patch("/todos/{todo_id}/toggle", response_model=schemas.Todo)
def toggle_todo(todo_id: int):
    todo = crud.toggle_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    ok = crud.delete_todo(todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None
