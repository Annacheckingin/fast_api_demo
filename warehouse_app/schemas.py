from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemCreate(BaseModel):
    name: str = Field(..., example="螺丝")
    quantity: int = Field(..., ge=0, example=100)
    location: Optional[str] = Field(None, example="A1-02")
    sku: Optional[str] = Field(None, example="SKU-001")


class Item(ItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
