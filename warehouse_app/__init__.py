from fastapi import FastAPI
from .routes import router

# 子应用不在自身路由上重复 `/warehouse` 前缀，主应用挂载时会提供前缀

__all__ = ["router"]
