from pydantic import BaseModel
from typing import List, Optional, Dict
from items.schemas.items import Item


class CartItem(Item):
    quantity: int


class Discount(BaseModel):
    code: Optional[str] = None


class CheckoutResponse(BaseModel):
    total_before_discount: float
    discount_amount: float
    total_after_discount: float
    applied_discount: Optional[str] = None


class AdminStats(BaseModel):
    total_items_purchased: int
    total_purchase_amount: float
    discount_codes: Dict[str, float]
    total_discount_amount: float
