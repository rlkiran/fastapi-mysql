from typing import List
from fastapi import APIRouter, HTTPException, Depends
from models import Item
from database import get_connection
from helpers import item_helper

item_routes = APIRouter()

@item_routes.get("/items/", response_model=List[dict])
async def list_items():
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM items")
        items = await cur.fetchall()
    conn.close()
    return [item_helper(item) for item in items]


@item_routes.post("/items/", response_model=dict)
async def create_item(item: Item):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (item.name, item.description))
        await conn.commit()
        item_id = cur.lastrowid
    conn.close()
    return {"id": item_id, "name": item.name, "description": item.description}

@item_routes.get("/items/{item_id}", response_model=dict)
async def read_item(item_id: int):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = await cur.fetchone()
    conn.close()
    if item:
        return item_helper(item)
    raise HTTPException(status_code=404, detail="Item not found")

@item_routes.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: int, item: Item):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("UPDATE items SET name = %s, description = %s WHERE id = %s", (item.name, item.description, item_id))
        await conn.commit()
    conn.close()
    return {"id": item_id, "name": item.name, "description": item.description}

@item_routes.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
        await conn.commit()
    conn.close()
    return {"id": item_id, "message": "Item deleted"}
