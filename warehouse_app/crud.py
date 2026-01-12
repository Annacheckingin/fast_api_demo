from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from db import engine
from .models import Item as ItemModel
from .schemas import ItemCreate


def list_items(limit: int = 100, offset: int = 0, name: Optional[str] = None) -> List[ItemModel]:
    with Session(engine) as session:
        stmt = select(ItemModel)
        if name:
            stmt = stmt.where(ItemModel.name.contains(name))
        stmt = stmt.offset(offset).limit(limit)
        return session.exec(stmt).all()


def create_item(data: ItemCreate) -> ItemModel:
    now = datetime.utcnow()
    item = ItemModel(
        name=data.name,
        quantity=data.quantity,
        location=data.location,
        sku=data.sku,
        created_at=now,
        updated_at=now,
    )
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def get_item(item_id: int) -> Optional[ItemModel]:
    with Session(engine) as session:
        return session.get(ItemModel, item_id)


def update_item(item_id: int, data: ItemCreate) -> Optional[ItemModel]:
    with Session(engine) as session:
        item = session.get(ItemModel, item_id)
        if not item:
            return None
        item.name = data.name
        item.quantity = data.quantity
        item.location = data.location
        item.sku = data.sku
        item.updated_at = datetime.utcnow()
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def delete_item(item_id: int) -> bool:
    with Session(engine) as session:
        item = session.get(ItemModel, item_id)
        if not item:
            return False
        session.delete(item)
        session.commit()
        return True
