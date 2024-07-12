from sqlalchemy.orm import Session
from app.repositories.item_repository import get_item, get_items, create_item
from app.schemas.items_schemas import ItemCreate


def create_new_item(db: Session, item: ItemCreate):
    return create_item(db, item)


def fetch_item(db: Session, item_id: int):
    return get_item(db, item_id)


def fetch_items(db: Session, skip: int = 0, limit: int = 10):
    return get_items(db, skip, limit)
