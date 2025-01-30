import pytest
import pytest_asyncio
from models import Item
from routes.item_routes import create_item, read_item, list_items, update_item, delete_item
from database import init_db, get_connection
from fastapi import HTTPException

# Mark the entire file for async tests
pytestmark = pytest.mark.asyncio

# Helper to initialize DB before running tests
@pytest_asyncio.fixture(scope="session")
async def setup_db():
    # Initialize DB for the test session
    await init_db()
    yield
    # Cleanup DB after tests (if needed)
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("DROP TABLE IF EXISTS items")
        await conn.commit()
    conn.close()

# Test creating an item
async def test_create_item(setup_db):
    test_item = {"name": "Test Item", "description": "A test description"}
    response = await create_item(Item(**test_item))
    assert response["name"] == "Test Item"
    assert response["description"] == "A test description"
    assert "id" in response

# Test reading an item
async def test_read_item(setup_db):
    test_item = {"name": "Read Item", "description": "Read description"}
    created_item = await create_item(Item(**test_item))
    response = await read_item(created_item["id"])
    assert response["name"] == "Read Item"
    assert response["description"] == "Read description"

# Test reading an item that doesn't exist
async def test_read_item_not_found(setup_db):
    with pytest.raises(HTTPException):
        await read_item(99999)  # Assuming this ID doesn't exist

# Test updating an item
async def test_update_item(setup_db):
    test_item = {"name": "Item to Update", "description": "Description to Update"}
    created_item = await create_item(Item(**test_item))
    
    updated_item = {"name": "Updated Item", "description": "Updated description"}
    response = await update_item(created_item["id"], Item(**updated_item))
    
    assert response["name"] == "Updated Item"
    assert response["description"] == "Updated description"

# Test deleting an item
async def test_delete_item(setup_db):
    test_item = {"name": "Item to Delete", "description": "Description to Delete"}
    created_item = await create_item(Item(**test_item))
    
    response = await delete_item(created_item["id"])
    assert response["id"] == created_item["id"]
    assert response["message"] == "Item deleted"

# Test deleting an item that doesn't exist
async def test_delete_item_not_found(setup_db):
    with pytest.raises(HTTPException):
        await delete_item(99999)  # Assuming this ID doesn't exist

# Test listing all items
async def test_list_items(setup_db):
    test_item1 = {"name": "Item 1", "description": "Description 1"}
    test_item2 = {"name": "Item 2", "description": "Description 2"}
    
    await create_item(Item(**test_item1))
    await create_item(Item(**test_item2))
    
    response = await list_items()
    assert len(response) >= 2
    assert any(item["name"] == "Item 1" for item in response)
    assert any(item["name"] == "Item 2" for item in response)
