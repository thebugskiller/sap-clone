import pytest
from fastapi.testclient import TestClient
import os
import io
from app.db.database import get_db, SessionLocal, Base, engine

def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_test_db(test_client):
    # Clear the database before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Override the get_db dependency
    test_client.app.dependency_overrides[get_db] = override_get_db
    yield
    test_client.app.dependency_overrides.clear()

def test_create_item(test_client, test_upload_dir):
    # Test creating item without file
    response = test_client.post(
        "/api/v1/items/",
        data={"name": "Test Item", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["image_path"] is None
    
    # Test creating item with file
    file_content = b"test file content"
    files = {
        "file": ("test.jpg", io.BytesIO(file_content), "image/jpeg")
    }
    response = test_client.post(
        "/api/v1/items/",
        data={"name": "Test Item", "description": "Test Description"},
        files=files
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["image_path"] is not None
    assert os.path.exists(data["image_path"])

def test_get_items(test_client):
    # Create test items
    for i in range(3):
        test_client.post(
            "/api/v1/items/",
            data={"name": f"Item {i}", "description": f"Description {i}"}
        )
    
    # Test getting all items
    response = test_client.get("/api/v1/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Test pagination
    response = test_client.get("/api/v1/items/?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_get_item(test_client):
    # Create test item
    response = test_client.post(
        "/api/v1/items/",
        data={"name": "Test Item", "description": "Test Description"}
    )
    item_id = response.json()["id"]
    
    # Test getting existing item
    response = test_client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Test Item"
    
    # Test getting non-existent item
    response = test_client.get("/api/v1/items/999")
    assert response.status_code == 404

def test_update_item(test_client, test_upload_dir):
    # Create test item
    response = test_client.post(
        "/api/v1/items/",
        data={"name": "Original Name", "description": "Original Description"}
    )
    item_id = response.json()["id"]
    
    # Test updating item
    response = test_client.put(
        f"/api/v1/items/{item_id}",
        data={"name": "Updated Name", "description": "Updated Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated Description"
    
    # Test updating with file
    file_content = b"test file content"
    files = {
        "file": ("test.jpg", io.BytesIO(file_content), "image/jpeg")
    }
    response = test_client.put(
        f"/api/v1/items/{item_id}",
        data={"name": "Updated Name", "description": "Updated Description"},
        files=files
    )
    assert response.status_code == 200
    data = response.json()
    assert data["image_path"] is not None
    assert os.path.exists(data["image_path"])

def test_delete_item(test_client, test_upload_dir):
    # Create test item with file
    file_content = b"test file content"
    files = {
        "file": ("test.jpg", io.BytesIO(file_content), "image/jpeg")
    }
    response = test_client.post(
        "/api/v1/items/",
        data={"name": "Test Item", "description": "Test Description"},
        files=files
    )
    item_id = response.json()["id"]
    file_path = response.json()["image_path"]
    
    # Test deleting item
    response = test_client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    
    # Verify item is deleted
    response = test_client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 404
    
    # Verify file is deleted
    assert not os.path.exists(file_path) 