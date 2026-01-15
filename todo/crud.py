from typing import Optional, List
from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import FastAPI, HTTPException
from database import engine
from todo.todo import Todo, TodoCreate


def create_todo(payload: TodoCreate):
	todo = Todo(title=payload.title, description=payload.description)
	with Session(engine) as session:
		session.add(todo)
		session.commit()
		session.refresh(todo)
		return todo


def list_todos():
	with Session(engine) as session:
		todos = session.exec(select(Todo)).all()
		print(f"获取到的待办事项: {todos}")
		return todos


def get_todo(todo_id: int):
	with Session(engine) as session:
		todo = session.get(Todo, todo_id)
		if not todo:
			raise HTTPException(status_code=404, detail="Todo not found")
		return todo


def update_todo(todo_id: int, payload: TodoCreate):
	with Session(engine) as session:
		todo = session.get(Todo, todo_id)
		if not todo:
			raise HTTPException(status_code=404, detail="Todo not found")
		todo.title = payload.title
		todo.description = payload.description
		session.add(todo)
		session.commit()
		session.refresh(todo)
		return todo


def toggle_todo(todo_id: int):
	with Session(engine) as session:
		todo = session.get(Todo, todo_id)
		if not todo:
			raise HTTPException(status_code=404, detail="Todo not found")
		todo.done = not todo.done
		session.add(todo)
		session.commit()
		session.refresh(todo)
		return todo


def delete_todo(todo_id: int):
	with Session(engine) as session:
		todo = session.get(Todo, todo_id)
		if not todo:
			raise HTTPException(status_code=404, detail="Todo not found")
		session.delete(todo)
		session.commit()
		return

