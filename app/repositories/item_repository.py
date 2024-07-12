from sqlalchemy.orm import Session
from app.models.items import Item
from app.schemas.items_schemas import ItemCreate


def get_item(db: Session, item_id: int):
    return db.query(Item).filter_by(id=item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
