from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.file_service import file_service
from typing import List, Optional

class ItemService:
    def create_item(self, db: Session, item: ItemCreate, file_path: Optional[str] = None) -> Item:
        db_item = Item(
            name=item.name,
            description=item.description,
            image_path=file_path
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
        return db.query(Item).offset(skip).limit(limit).all()

    def get_item(self, db: Session, item_id: int) -> Item:
        item = db.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def update_item(
        self, 
        db: Session, 
        item_id: int, 
        item: ItemUpdate, 
        file_path: Optional[str] = None
    ) -> Item:
        db_item = self.get_item(db, item_id)
        
        # Delete old file if new file is uploaded
        if file_path and db_item.image_path:
            file_service.delete_file(db_item.image_path)

        # Update item
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        
        if file_path:
            db_item.image_path = file_path

        db.commit()
        db.refresh(db_item)
        return db_item

    def delete_item(self, db: Session, item_id: int) -> None:
        db_item = self.get_item(db, item_id)
        
        # Delete associated file
        if db_item.image_path:
            file_service.delete_file(db_item.image_path)
        
        db.delete(db_item)
        db.commit()

item_service = ItemService() 