from typing import List
import aiomysql
from fastapi import APIRouter, HTTPException
from models import Item
from database import get_connection
from helpers import item_helper

item_routes = APIRouter()

# Route to list all items
@item_routes.get("/items/", response_model=List[dict])
async def list_items():
    try:
        conn = await get_connection()
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM items")
            items = await cur.fetchall()
        conn.close()
        return [item_helper(item) for item in items]
    except aiomysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")

# Route to create a new item
@item_routes.post("/items/", response_model=dict)
async def create_item(item: Item):
    try:
        conn = await get_connection()
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (item.name, item.description))
            await conn.commit()
            item_id = cur.lastrowid
        conn.close()
        return {"id": item_id, "name": item.name, "description": item.description}
    except aiomysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error inserting item: {str(e)}")

# Route to read a single item
@item_routes.get("/items/{item_id}", response_model=dict)
async def read_item(item_id: int):
    try:
        conn = await get_connection()
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = await cur.fetchone()
        conn.close()
        if item:
            return item_helper(item)
        raise HTTPException(status_code=404, detail="Item not found")
    except aiomysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error reading item: {str(e)}")

# Route to update an item
@item_routes.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: int, item: Item):
    try:
        conn = await get_connection()
        async with conn.cursor() as cur:
            await cur.execute("UPDATE items SET name = %s, description = %s WHERE id = %s", (item.name, item.description, item_id))
            await conn.commit()
        conn.close()
        return {"id": item_id, "name": item.name, "description": item.description}
    except aiomysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error updating item: {str(e)}")

# Route to delete an item
# @item_routes.delete("/items/{item_id}", response_model=dict)
# async def delete_item(item_id: int):
#     try:
#         conn = await get_connection()
#         async with conn.cursor() as cur:
#             await cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
#             await conn.commit()
#         conn.close()
#         return {"id": item_id, "message": "Item deleted"}
#     except aiomysql.MySQLError as e:
#         raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")
@item_routes.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = await cur.fetchone()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        await cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
        await conn.commit()

    conn.close()
    return {"id": item_id, "message": "Item deleted"}

