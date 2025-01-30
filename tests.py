import pytest
from models import Item
from routes.item_routes import create_item, read_item

pytestmark = pytest.mark.asyncio(loop_scope="session")

async def test_create_item():
    test_item = {"name": "Test Item", "description": "A test description"}
    response = await create_item(Item(**test_item))
    assert response["name"] == "Test Item"
    assert response["description"] == "A test description"

async def test_read_item():
    test_item = {"name": "Read Item", "description": "Read description"}
    created_item = await create_item(Item(**test_item))
    response = await read_item(created_item["id"])
    assert response["name"] == "Read Item"
    assert response["description"] == "Read description"
