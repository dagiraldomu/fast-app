from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.items_schemas import Item, ItemCreate
from app.services.items_service import create_new_item, fetch_item, fetch_items
from app.models.items import get_db


# Define router object
router = APIRouter(
    prefix="/items",  # Add a prefix for all routes in this file
    tags=["items"],  # Tags for documentation purposes
)


@router.post("/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
        Create a new item.

        This endpoint allows for the creation of a new item with the given name and price.

        Parameters:
        - item: ItemCreate - A Pydantic model containing the name and price of the new item.
        - db: Session - The database session dependency.

        Returns:
        - Item: A Pydantic model representing the created item.
    """
    return create_new_item(db, item)


@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
        Retrieve a list of items.

        This endpoint returns a list of items from the database with pagination support.

        Parameters:
        - skip: int - The number of records to skip for pagination (default is 0).
        - limit: int - The maximum number of records to return (default is 10).
        - db: Session - The database session dependency.

        Returns:
        - List[Item]: A list of Pydantic models representing the items.
    """
    return fetch_items(db, skip, limit)


@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
        Retrieve a specific item by ID.

        This endpoint returns an item based on the provided item ID.

        Parameters:
        - item_id: int - The ID of the item to retrieve.
        - db: Session - The database session dependency.

        Returns:
        - Item: A Pydantic model representing the retrieved item.

        Raises:
        - HTTPException: If the item with the specified ID is not found, a 404 error is raised.
    """
    item = fetch_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

