import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_register_and_login_flow():
    reg_payload = {
        "email": "promoter@precisiongears.in",
        "password": "Password123!",
        "full_name": "Ramesh Kumar",
        "role": "msme",
        "jurisdiction": "Karnataka"
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 200
    data = reg_res.json()
    assert "access_token" in data
    assert data["role"] == "msme"

    login_payload = {
        "email": "promoter@precisiongears.in",
        "password": "Password123!"
    }
    login_res = client.post("/api/auth/login", json=login_payload)
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

def test_duplicate_registration_fails():
    reg_payload = {
        "email": "admin@karnataka.gov.in",
        "password": "Password123!",
        "full_name": "Officer Desk",
        "role": "admin",
        "jurisdiction": "Karnataka"
    }
    client.post("/api/auth/register", json=reg_payload)
    dup_res = client.post("/api/auth/register", json=reg_payload)
    assert dup_res.status_code == 400
