from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    name: str
    category: str
    price: float


class Item(ItemBase):
    id: int


class ItemCreate(Item):
    inventory: int


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    inventory: Optional[int] = None
