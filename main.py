
import os
import alembic.command as alembic_cmd
from click import command
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.utils import get_openapi
from sqlmodel import SQLModel
from alembic.config import Config
from database.database import engine as engine
from todo.crud import create_todo, list_todos, get_todo, update_todo, toggle_todo, delete_todo
from todo.todo import Todo
from typing import List
import os

def run_migrations():
    ini_path = os.path.join(os.getcwd(), "alembic.ini")
    
    alembic_cfg = Config(ini_path)
    
    # 核心修复：使用别名调用 upgrade
    alembic_cmd.upgrade(alembic_cfg, "head")

# 定义生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ------------------ 启动时运行 ------------------
    print("正在检查并运行数据库迁移...")
    try:
        run_migrations()
        print("数据库迁移完成！")
    except Exception as e:
        print(f"迁移失败: {e}")
        print("正在创建数据库表...")
        SQLModel.metadata.create_all(engine)
        print("数据库表创建完成！")
    
    yield  # 这里是 FastAPI 运行的地方
    
    # ------------------ 关闭时运行 ------------------
    print("正在关闭服务...")
    
app = FastAPI(
	title="Simple ToDo App (SQLModel)",
	description="A simple ToDo API using FastAPI and SQLModel.",
	version="0.1.0",
	docs_url="/swagger",
	redoc_url="/redoc",
	openapi_url="/openapi.json",
	lifespan=lifespan,
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


