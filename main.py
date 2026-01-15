
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from sqlmodel import SQLModel
from database import engine
from todo.crud import create_todo, list_todos, get_todo, update_todo, toggle_todo, delete_todo
from todo.todo import TodoCreate, Todo
from typing import List

app = FastAPI(
	title="Simple ToDo App (SQLModel)",
	description="A simple ToDo API using FastAPI and SQLModel.",
	version="0.1.0",
	docs_url="/swagger",
	redoc_url="/redoc",
	openapi_url="/openapi.json",
)

@app.on_event("startup")
def on_startup():
	SQLModel.metadata.create_all(engine)


def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema = get_openapi(
		title=app.title,
		version=app.version,
		description=app.description,
		routes=app.routes,
	)
	openapi_schema["info"]["x-logo"] = {
		"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
	}
	app.openapi_schema = openapi_schema
	return app.openapi_schema


app.openapi = custom_openapi

# Register routes
app.post("/todos", response_model=Todo)(create_todo)
app.get("/todos", response_model=List[Todo])(list_todos)
app.get("/todos/{todo_id}", response_model=Todo)(get_todo)
app.put("/todos/{todo_id}", response_model=Todo)(update_todo)
app.patch("/todos/{todo_id}/toggle", response_model=Todo)(toggle_todo)
app.delete("/todos/{todo_id}", status_code=204)(delete_todo)


