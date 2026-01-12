# Simple FastAPI ToDo Demo

这是一个最小的 ToDo 应用示例，基于 FastAPI，使用内存存储（仅用于演示）。

快速开始：

1. 创建并激活虚拟环境（可选但推荐）

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. 安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

3. 启动服务器：

```bash
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API 示例：

- 创建 Todo：

```bash
curl -X POST "http://127.0.0.1:8000/todos" -H "Content-Type: application/json" -d '{"title":"Buy milk","description":"2 liters"}'
```

- 列表 Todos：

```bash
curl http://127.0.0.1:8000/todos
```

- 切换完成状态：

```bash
curl -X PATCH http://127.0.0.1:8000/todos/<id>/toggle
```

更多扩展建议：

- 使用数据库（SQLite/Postgres）替换内存存储
- 添加用户认证和授权
- 添加持久化迁移和测试
