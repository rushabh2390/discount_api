from fastapi import HTTPException, Depends, APIRouter
from typing import Optional, List
from utils.utils import generate_discount_code
from orders.schemas import orders as order_schemas
from users.schemas import users as user_schemas
from users.routers.users import get_current_user
from databases.database import data

router = APIRouter(prefix="/orders")


@router.post("/cart", response_model=List[order_schemas.CartItem], status_code=200)
async def add_to_cart(item: order_schemas.CartItem):
    data.cart.append(item.model_dump())
    # inventory calculation is not added here..
    return data.cart


@router.get("/cart", response_model=List[order_schemas.CartItem], status_code=200)
async def view_cart():
    return data.cart


@router.post("/checkout", response_model=order_schemas.CheckoutResponse, status_code=200)
async def checkout(discount: Optional[order_schemas.Discount] = None):
    total_before_discount = sum(
        item["price"] * item["quantity"] for item in data.cart)
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
        "items": data.cart.copy(),
        "total_amount": total_after_discount,
        "discount_code": applied_discount,
    }
    data.orders.append(order)
    data.cart.clear()  # clear cart after checkout.

    if len(data.orders) % data.nth_order == 0:
        if applied_discount is None:  # only generate new code if a previous code wasn't used.
            applied_discount = generate_discount_code(data.discount_value)
            data.orders[-1]["discount_code"] = applied_discount
            data.used_discount_codes[applied_discount] = data.discount_value
            discount_amount = total_before_discount * data.discount_value
            total_after_discount = total_before_discount - discount_amount
            return order_schemas.CheckoutResponse(
                total_before_discount=total_before_discount,
                discount_amount=discount_amount,
                total_after_discount=total_after_discount,
                applied_discount=applied_discount,
            )
    return order_schemas.CheckoutResponse(
        total_before_discount=total_before_discount,
        discount_amount=discount_amount,
        total_after_discount=total_after_discount,
        applied_discount=applied_discount,
    )


@router.delete("/cart/clear", status_code=200)
async def clear_cart():
    data.cart.clear()
    return {"message": "Cart cleared"}


@router.get("/orders", status_code=200)
async def get_orders():
    return data.orders


@router.get("/discount_code", response_model=Optional[order_schemas.Discount])
async def generate_admin_discount_code(order_number: int):
    """Generates a discount code if the nth order condition is met"""
    if order_number % data.nth_order == 0:
        discount_value = 0.10
        code = generate_discount_code(discount_value)
        return order_schemas.Discount(code=code)
    else:
        return None


@router.get("/stats", response_model=order_schemas.AdminStats)
async def get_admin_stats(current_user: user_schemas.TokenData = Depends(get_current_user)):
    """Returns admin statistics."""
    if current_user.is_admin:
        total_items_purchased = 0
        total_purchase_amount = 0.0
        total_discount_amount = 0.0
        used_discount_codes = {}
        for order in data.orders:
            total_items_purchased += sum(item["quantity"]
                                         for item in order["items"])
            total_purchase_amount += order["total_amount"]
            if order["discount_code"] in data.discount_codes and order["discount_code"] is not None:
                code = order["discount_code"]
                used_discount_codes[code] = data.discount_codes[code] * sum(item["price"] * item["quantity"]
                                                                            for item in order["items"])
                total_discount_amount += used_discount_codes[code]
        return order_schemas.AdminStats(
            total_items_purchased=total_items_purchased,
            total_purchase_amount=total_purchase_amount,
            discount_codes=used_discount_codes,
            total_discount_amount=total_discount_amount,
        )
    raise HTTPException(
        status_code=403, detail="Only admin can get stats")
