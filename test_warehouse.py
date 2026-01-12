from fastapi.testclient import TestClient
import sys
from main import app

client = TestClient(app)

def check(resp, expect_code=200):
    print(resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print("<no-json>")

print("== GET /warehouse/items ==")
r = client.get("/warehouse/items")
check(r)

print("== POST /warehouse/items ==")
r = client.post("/warehouse/items", json={"name":"螺丝","quantity":10,"location":"A1"})
check(r, 201)
if r.status_code not in (200,201):
    print('POST failed')
    sys.exit(2)
created = r.json()
item_id = created.get('id')
if not item_id:
    print('no id returned')
    sys.exit(3)

print(f"== GET /warehouse/items/{item_id} ==")
r = client.get(f"/warehouse/items/{item_id}")
check(r)

print(f"== PUT /warehouse/items/{item_id} ==")
r = client.put(f"/warehouse/items/{item_id}", json={"name":"螺丝X","quantity":5,"location":"B2"})
check(r)

print(f"== DELETE /warehouse/items/{item_id} ==")
r = client.delete(f"/warehouse/items/{item_id}")
print(r.status_code)

print("== FINAL LIST ==")
r = client.get("/warehouse/items")
check(r)

print('ALL_OK')
