from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import item_service
from app.services.file_service import file_service

router = APIRouter()

@router.post("/", response_model=Item)
async def create_item(
    name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    file_path = file_service.save_file(file) if file else None
    item = ItemCreate(name=name, description=description)
    return item_service.create_item(db, item, file_path)

@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return item_service.get_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    return item_service.get_item(db, item_id)

@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    file_path = file_service.save_file(file) if file else None
    item = ItemUpdate(name=name, description=description)
    return item_service.update_item(db, item_id, item, file_path)

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item_service.delete_item(db, item_id)
    return {"message": "Item deleted successfully"} 