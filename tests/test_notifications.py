import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app  # Adjust this import to wherever your FastAPI app instance lives
from app.api.deps import get_current_user, get_current_admin_user
from app.models.notification import Notification
from app.models.user import User

# Quick mock generators for authentication dependencies
def mock_admin_user():
    return User(id=1, username="admin", is_admin=True, score=0)

def mock_normal_user():
    return User(id=2, username="player1", is_admin=False, score=0)


def test_admin_can_send_notification(client: TestClient, db_session: Session):
    # Override dependency to simulate an admin login
    app.dependency_overrides[get_current_admin_user] = mock_admin_user
    
    payload = {"content": "System maintenance in 10 minutes!"}
    response = client.post("/api/v1/admin/notifications", json=payload)
    
    # Clean up overrides right away
    app.dependency_overrides.clear()
    
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == payload["content"]


def test_player_can_receive_notifications(client: TestClient, db_session: Session):
    app.dependency_overrides[get_current_user] = mock_normal_user
    
    # Seed data using the correct 'db_session' fixture name from your logs
    test_notification = Notification(content="Welcome to NexusFlag v1.0.0!")
    db_session.add(test_notification)
    db_session.commit()

    response = client.get("/api/v1/game/notifications")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()[0]["content"] == "Welcome to NexusFlag v1.0.0!"


def test_player_cannot_send_notification(client: TestClient):
    app.dependency_overrides[get_current_user] = mock_normal_user
    
    payload = {"content": "Hacking attempts..."}
    response = client.post("/api/v1/admin/notifications", json=payload)
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 403

def test_notification_character_limit(client: TestClient):
    app.dependency_overrides[get_current_admin_user] = mock_admin_user
    
    payload = {"content": "A" * 281}
    response = client.post("/api/v1/admin/notifications", json=payload)
    app.dependency_overrides.clear()

    assert response.status_code == 422
