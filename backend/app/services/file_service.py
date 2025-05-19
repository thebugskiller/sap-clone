import os
import shutil
from datetime import datetime
from fastapi import UploadFile, HTTPException
from typing import Optional

class FileService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

    def save_file(self, file: UploadFile) -> str:
        """Save an uploaded file and return its path."""
        if not file:
            return None

        # Validate file type
        allowed_types = ["image/png", "image/jpeg", "image/bmp"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="File type not allowed")

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(self.upload_dir, filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

    def delete_file(self, file_path: Optional[str]) -> None:
        """Delete a file if it exists."""
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

file_service = FileService() 