import pytest
from fastapi import UploadFile, HTTPException
import os
import io

def test_save_file(file_service):
    # Test saving valid file
    content = b"test file content"
    file = UploadFile(
        file=io.BytesIO(content),
        filename="test.jpg",
        headers={"content-type": "image/jpeg"}
    )
    
    file_path = file_service.save_file(file)
    assert file_path is not None
    assert os.path.exists(file_path)
    
    # Verify file content
    with open(file_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == content

def test_save_invalid_file_type(file_service):
    # Test saving invalid file type
    content = b"test file content"
    file = UploadFile(
        file=io.BytesIO(content),
        filename="test.txt",
        headers={"content-type": "text/plain"}
    )
    
    with pytest.raises(HTTPException) as exc_info:
        file_service.save_file(file)
    assert exc_info.value.status_code == 400
    assert "File type not allowed" in str(exc_info.value.detail)

def test_save_no_file(file_service):
    # Test saving None file
    file_path = file_service.save_file(None)
    assert file_path is None

def test_delete_file(file_service):
    # Test deleting existing file
    file_path = os.path.join(file_service.upload_dir, "test.jpg")
    with open(file_path, "w") as f:
        f.write("test content")
    
    file_service.delete_file(file_path)
    assert not os.path.exists(file_path)
    
    # Test deleting non-existent file
    file_service.delete_file("non_existent.jpg")  # Should not raise an error

def test_delete_none_file(file_service):
    # Test deleting None file path
    file_service.delete_file(None)  # Should not raise an error 