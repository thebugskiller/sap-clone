import pytest
from app.services.item_service import ItemService
from app.schemas.item import ItemCreate, ItemUpdate
from fastapi import HTTPException
import os

def test_create_item(db_session, file_service):
    service = ItemService()
    item_data = ItemCreate(name="Test Item", description="Test Description")
    
    # Test creating item without file
    item = service.create_item(db_session, item_data)
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert item.image_path is None

    # Test creating item with file
    file_path = "test_uploads/test.jpg"
    with open(file_path, "w") as f:
        f.write("test content")
    
    item_with_file = service.create_item(db_session, item_data, file_path)
    assert item_with_file.name == "Test Item"
    assert item_with_file.image_path == file_path

def test_get_items(db_session):
    service = ItemService()
    
    # Create test items
    items = [
        ItemCreate(name=f"Item {i}", description=f"Description {i}")
        for i in range(3)
    ]
    for item in items:
        service.create_item(db_session, item)
    
    # Test getting all items
    all_items = service.get_items(db_session)
    assert len(all_items) == 3
    
    # Test pagination
    paginated_items = service.get_items(db_session, skip=1, limit=1)
    assert len(paginated_items) == 1

def test_get_item(db_session):
    service = ItemService()
    
    # Create test item
    item_data = ItemCreate(name="Test Item", description="Test Description")
    created_item = service.create_item(db_session, item_data)
    
    # Test getting existing item
    item = service.get_item(db_session, created_item.id)
    assert item.id == created_item.id
    assert item.name == "Test Item"
    
    # Test getting non-existent item
    with pytest.raises(HTTPException) as exc_info:
        service.get_item(db_session, 999)
    assert exc_info.value.status_code == 404

def test_update_item(db_session, file_service):
    service = ItemService()
    
    # Create test item
    item_data = ItemCreate(name="Original Name", description="Original Description")
    created_item = service.create_item(db_session, item_data)
    
    # Test updating item
    update_data = ItemUpdate(name="Updated Name", description="Updated Description")
    updated_item = service.update_item(db_session, created_item.id, update_data)
    assert updated_item.name == "Updated Name"
    assert updated_item.description == "Updated Description"
    
    # Test updating with file
    file_path = "test_uploads/test.jpg"
    with open(file_path, "w") as f:
        f.write("test content")
    
    updated_with_file = service.update_item(db_session, created_item.id, update_data, file_path)
    assert updated_with_file.image_path == file_path

def test_delete_item(db_session, file_service):
    service = ItemService()
    
    # Create test item with file
    item_data = ItemCreate(name="Test Item", description="Test Description")
    file_path = "test_uploads/test.jpg"
    with open(file_path, "w") as f:
        f.write("test content")
    
    created_item = service.create_item(db_session, item_data, file_path)
    
    # Test deleting item
    service.delete_item(db_session, created_item.id)
    
    # Verify item is deleted
    with pytest.raises(HTTPException) as exc_info:
        service.get_item(db_session, created_item.id)
    assert exc_info.value.status_code == 404
    
    # Verify file is deleted
    assert not os.path.exists(file_path) 