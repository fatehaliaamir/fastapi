from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLE = "consumables"

class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category

items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=9.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=9.99, count=20, id=2, category=Category.CONSUMABLE),
}

############################
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}

############################
@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        error_message = {"error": f"Item with id {item_id} does not exist"}
        return JSONResponse(content=error_message, status_code=404)
    return items[item_id]

# @app.get("/items/")
# def get_all_items() -> dict[str, dict[int, Item]]:
#     return {"items": items}

############################
@app.get("/items/")
def get_items(
    name: Optional[str] = None,
    price: Optional[float] = None,
    count: Optional[int] = None,
    category: Optional[Category] = None,
) -> dict[str, dict[int, Item]]:
    filtered_items = {
        item.id: item
        for item in items.values()
        if (name is None or item.name == name)
        and (price is None or item.price == price)
        and (count is None or item.count == count)
        and (category is None or item.category == category)
    }

    return {"filtered_items": filtered_items}

############################
@app.post("/")
def add_item(item: Item) -> dict[str, Item]:
    
    if item.id in item:
        error_message = {"error": f"Item with id {item_id} does not exist"}
        return JSONResponse(content=error_message, status_code=404)
    
    items[item.id] = item
    return {"added": item}

############################
@app.put("/items/{item_id}")
def update(
    item_id: int,
    name: Optional[str] = Query(None, min_length=1),
    price: Optional[float] = Query(None, ge=0),
    count: Optional[int] = Query(None, ge=0),
) -> dict[str, str]:
    if item_id not in items:
        error_message = {"error": f"Item with id {item_id} does not exist"}
        return JSONResponse(content=error_message, status_code=404)

    # Get the item
    item = items[item_id]

    # Update the item with provided values
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"message": f"Item with id {item_id} updated"}
    
############################
@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:

    if item_id not in items:
        error_message = {"error": f"Item with id {item_id} does not exist"}
        return JSONResponse(content=error_message, status_code=404)
    
    item = items.pop(item_id)
    return {"deleted": item}