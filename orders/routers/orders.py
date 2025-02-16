from fastapi import HTTPException, Depends, APIRouter
from typing import Optional, List
from utils.utils import generate_discount_code
from orders.schemas import orders as orders_schemas
from databases.database import data

router = APIRouter(prefix="/orders")
cart = []


@router.post("/cart", response_model=orders_schemas.CartItem)
async def add_to_cart(item: orders_schemas.Item):
    cart.append(item.model_dump())
    return item


@router.get("/cart", response_model=List[orders_schemas.CartItem])
async def view_cart():
    return cart


@router.post("/checkout", response_model=orders_schemas.CheckoutResponse)
async def checkout(discount: Optional[orders_schemas.Discount] = None):
    total_before_discount = sum(
        item["price"] * item["quantity"] for item in cart)
    discount_amount = 0.0
    applied_discount = None

    if discount:
        if discount.code in data.discount_codes:
            discount_percentage = data.discount_codes[discount.code]
            discount_amount = total_before_discount * discount_percentage
            applied_discount = discount.code
        else:
            raise HTTPException(
                status_code=400, detail="Invalid discount code")

    total_after_discount = total_before_discount - discount_amount

    order = {
        "items": cart,
        "total_amount": total_after_discount,
        "discount_code": applied_discount,
    }
    data.orders.append(order)
    cart.clear()  # clear cart after checkout.

    if len(data.orders) % data.nth_order == 0:
        if applied_discount is None:  # only generate new code if a previous code wasn't used.
            discount_value = 0.10  # 10% discount
            code = generate_discount_code(discount_value)
            data.orders[-1]["discount_code"] = code
            return orders_schemas.CheckoutResponse(
                total_before_discount=total_before_discount,
                discount_amount=discount_amount,
                total_after_discount=total_after_discount,
                applied_discount=applied_discount,
            )
    return orders_schemas.CheckoutResponse(
        total_before_discount=total_before_discount,
        discount_amount=discount_amount,
        total_after_discount=total_after_discount,
        applied_discount=applied_discount,
    )


@router.delete("/cart/clear")
async def clear_cart():
    cart.clear()
    return {"message": "Cart cleared"}
