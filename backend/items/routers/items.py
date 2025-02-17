from fastapi import HTTPException, Depends, APIRouter
from typing import Optional, List
from items.schemas import items as items_schemas
from databases.database import data

router = APIRouter(prefix="/items")


@router.get("/", response_model=List[items_schemas.ItemCreate])
async def get_items(category: Optional[str] = None):
    cat_items = []
    if category:
        for item in data.items:
            if item["category"] == category:
                cat_items.append(item)
    else:
        return data.items
    if not cat_items:
        raise HTTPException(status_code=404, detail="item not found")
    return cat_items


@router.post("/", response_model=items_schemas.ItemCreate)
async def create_item(item: items_schemas.ItemCreate):
    new_item = item.model_dump()
    new_item["id"] = data.max_item_id
    data.max_item_id += 1
    data.items.append(new_item)
    return new_item


@router.patch("/{id}", response_model=items_schemas.ItemCreate)
async def update_item(id: int, item: items_schemas.ItemUpdate):
    existing_item = None
    for item in data.items:
        if item["id"] == id:
            existing_item = item
            break
    if not existing_item:
        raise HTTPException(status_code=404, detail="item not found")
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(existing_item, key, value)
    return existing_item
