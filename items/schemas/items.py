from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    name: str
    category: str
    price: float
    inventory: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    inventory: Optional[int] = None


class Item(ItemBase):
    id: int
