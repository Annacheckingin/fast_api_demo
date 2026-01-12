from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from . import crud, schemas

router = APIRouter()


@router.get("/items", response_model=List[schemas.Item])
def read_items(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    name: Optional[str] = Query(None),
):
    return crud.list_items(limit=limit, offset=offset, name=name)


@router.post("/items", response_model=schemas.Item, status_code=201)
def create_item(item: schemas.ItemCreate):
    return crud.create_item(item)


@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int):
    it = crud.get_item(item_id)
    if not it:
        raise HTTPException(status_code=404, detail="Item not found")
    return it


@router.put("/items/{item_id}", response_model=schemas.Item)
def put_item(item_id: int, item: schemas.ItemCreate):
    it = crud.update_item(item_id, item)
    if not it:
        raise HTTPException(status_code=404, detail="Item not found")
    return it


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    ok = crud.delete_item(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
