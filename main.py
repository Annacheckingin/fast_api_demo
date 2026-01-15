
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.utils import get_openapi
from typing import Optional, List
from sqlmodel import SQLModel, Field
from db import engine
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def tai_init(app:FastAPI):
	print("Starting up the application...")
	yield
	print("Shutting down the application...")
app = FastAPI(
	title="Simple ToDo App (SQLModel)",
	description="A simple ToDo API using FastAPI and SQLModel.",
	version="0.1.0",
	docs_url="/swagger",
	redoc_url="/redoc",
	openapi_url="/openapi.json",
	lifespan=tai_init
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],  # 或 ["*"]（开发时慎用）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ToDo 已提取为子应用 `todo_app`（见 todo_app/）



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
    

class MyOpen:
	def __init__(self, filePath):
		print('entering the constuctor')
		print(filePath)
		pass

	def __enter__(self):
		print('entering the _enter_ method')
		pass
	def __exsit__(self, exc_type, exc_val, exc_tb):
		print('entering the  exisit method')
		pass

with MyOpen('path/to/file') as f:
	print('inside the with block')	