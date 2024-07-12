import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.items import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_create_item():
    response = client.post("/items/", json={"name": "Watch", "price": 39.99})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Watch"
    assert data["price"] == 39.99
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_read_items():
    #client.post("/items/", json={"name": "Watch", "price": 39.99})
    client.post("/items/", json={"name": "Glasses", "price": 19.99})

    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Watch"
    assert data[1]["name"] == "Glasses"


def test_read_item():
    response = client.post("/items/", json={"name": "Watch", "price": 39.99})
    item_id = response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Watch"
    assert data["price"] == 39.99
    assert data["id"] == item_id
