from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import Base, get_db
import app.models
from app.main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def override_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_db
client = TestClient(app)

def headers():
    r = client.post("/api/v1/auth/register", json={"email":"api@example.com","username":"apiuser","password":"StrongPass123!"})
    if r.status_code == 409:
        r = client.post("/api/v1/auth/login", json={"email":"api@example.com","password":"StrongPass123!"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}

def test_auth_and_me():
    h = headers()
    assert client.get("/api/v1/auth/me", headers=h).status_code == 200

def test_mood_and_diary_are_user_scoped():
    h = headers()
    assert client.post("/api/v1/moods", headers=h, json={"mood":"Good","stress":2,"energy":4}).status_code == 201
    assert client.post("/api/v1/diary", headers=h, json={"title":"Today","content":"A small reflection."}).status_code == 201
    assert len(client.get("/api/v1/moods", headers=h).json()) >= 1
    assert len(client.get("/api/v1/diary", headers=h).json()) >= 1

def test_bloom_high_risk_is_intercepted():
    h = headers()
    r = client.post("/api/v1/bloom/chat", headers=h, json={"message":"I want to kill myself"})
    assert r.status_code == 200
    assert r.json()["risk_level"] == "HIGH_RISK"
    assert r.json()["safety_escalation"] is True
    assert r.json()["provider"] == "safety-policy"

def test_demo_session_is_available():
    r = client.post("/api/v1/demo/session")
    assert r.status_code == 200
    assert r.json()["demo"] is True
