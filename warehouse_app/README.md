# warehouse_app 子应用

这是一个演示用的仓储管理子应用，使用内存存储（仅用于开发/演示）。

可用接口（挂载路径 `/warehouse`）：

- `GET /warehouse/items` - 列表所有物料
- `POST /warehouse/items` - 创建物料（body: `name`, `quantity`, `location`）
 - `POST /warehouse/items` - 创建物料（body: `name`, `quantity`, `location`, `sku`）
- `GET /warehouse/items/{item_id}` - 获取单个物料
- `PUT /warehouse/items/{item_id}` - 更新物料
- `DELETE /warehouse/items/{item_id}` - 删除物料

额外字段:
- `sku` (可选): 物料编码
- `created_at` / `updated_at`: 自动生成的时间戳（UTC）

列表接口支持分页与按名称模糊过滤: `GET /warehouse/items?limit=50&offset=0&name=螺`

在生产中请替换 `crud.py` 中的存储为数据库实现。
