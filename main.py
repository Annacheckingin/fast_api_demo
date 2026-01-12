
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from typing import Optional, List
from sqlmodel import SQLModel, Field


app = FastAPI(
	title="Simple ToDo App (SQLModel)",
	description="A simple ToDo API using FastAPI and SQLModel.",
	version="0.1.0",
	docs_url="/swagger",
	redoc_url="/redoc",
	openapi_url="/openapi.json",
)
# ToDo 已提取为子应用 `todo_app`（见 todo_app/）

from db import engine


@app.on_event("startup")
def on_startup():
	# 在启动时创建所有表（包括子应用定义的模型）
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


# Include routers from sub-applications so their operations appear in the main OpenAPI
from warehouse_app import router as warehouse_router
app.include_router(warehouse_router, prefix="/warehouse")

# Include todo router
from todo_app import router as todo_router
app.include_router(todo_router, prefix="/todos")
    

