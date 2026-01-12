# todo_app 子应用

把原来 `main.py` 中的 ToDo 功能提取为子应用，挂载路径为 `/todos`。

接口：

- `POST /todos` - 创建 ToDo（body: `title`, `description`）
- `GET /todos` - 列表 ToDo
- `GET /todos/{todo_id}` - 获取单个 ToDo
- `PUT /todos/{todo_id}` - 更新 ToDo
- `PATCH /todos/{todo_id}/toggle` - 切换完成状态
- `DELETE /todos/{todo_id}` - 删除 ToDo
