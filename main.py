
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from typing import Optional, List
from sqlmodel import SQLModel, Field, Session, create_engine, select


app = FastAPI(
	title="Simple ToDo App (SQLModel)",
	description="A simple ToDo API using FastAPI and SQLModel.",
	version="0.1.0",
	docs_url="/swagger",
	redoc_url="/redoc",
	openapi_url="/openapi.json",
)


class Todo(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	title: str
	description: Optional[str] = None
	done: bool = False


class TodoCreate(SQLModel):
	title: str
	description: Optional[str] = None


# SQLite engine (file-based). For tests/dev use, file is `database.db` in workspace.
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False)


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


@app.post("/todos", response_model=Todo)
def create_todo(payload: TodoCreate):
	todo = Todo(title=payload.title, description=payload.description)
	with Session(engine) as session:
		session.add(todo)
		session.commit()
		session.refresh(todo)
		return todo


@app.get("/todos", response_model=List[Todo])
def list_todos():
	with Session(engine) as session:
		todos = session.exec(select(Todo)).all()
		return todos


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
	with Session(engine) as session:
		todo = session.get(Todo, todo_id)
		if not todo:
			raise HTTPException(status_code=404, detail="Todo not found")
		return todo


@app.put("/todos/{todo_id}", response_model=Todo)
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


@app.patch("/todos/{todo_id}/toggle", response_model=Todo)
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


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
	with Session(engine) as session:
		todo = session.get(Todo, todo_id)
		if not todo:
			raise HTTPException(status_code=404, detail="Todo not found")
		session.delete(todo)
		session.commit()
		return

