import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.api.deps import get_current_user
from app.core.limiter import limiter
from app.models.settings import SystemConfig
from app.models.user import User


def mock_admin_user():
    return User(id=1, username="admin", is_admin=True, score=0)


def mock_normal_user():
    return User(id=2, username="player1", is_admin=False, score=0)


@pytest.fixture(autouse=True)
def reset_limiter_and_db_session(monkeypatch, db_session: Session):
    """
    1. Ensures SlowAPI's internal DB lookups use the test db_session.
    2. Resets in-memory hit counters before and after every test.
    3. Ensures rate limiting starts enabled with tight test thresholds.
    """
    monkeypatch.setattr("app.core.limiter.SessionLocal", lambda: db_session)
    # Prevent SlowAPI's `with SessionLocal()` block from closing the shared test session
    monkeypatch.setattr(db_session, "close", lambda: None)

    limiter.enabled = True
    limiter.reset()

    # Seed default rate limit config in the test DB
    config = db_session.query(SystemConfig).filter(SystemConfig.id == 1).first()
    if not config:
        config = SystemConfig(
            id=1,
            rate_limit_enabled=True,
            login_rate_limit="3/minute",
            submit_rate_limit="2/minute",
        )
        db_session.add(config)
    else:
        config.rate_limit_enabled = True
        config.login_rate_limit = "3/minute"
        config.submit_rate_limit = "2/minute"
    db_session.commit()

    yield

    limiter.reset()
    app.dependency_overrides.clear()


## 1. Test: /login enforces rate limit and returns 429 when exceeded
def test_login_rate_limit_enforced(client: TestClient):
    login_payload = {"username": "nonexistent", "password": "wrongpassword"}

    # First 3 requests are within the "3/minute" limit (should return 401/400, NOT 429)
    for _ in range(3):
        response = client.post("/api/v1/auth/login", data=login_payload)
        assert response.status_code != 429

    # 4th request exceeds "3/minute" -> 429 Too Many Requests
    blocked_response = client.post("/api/v1/auth/login", data=login_payload)
    assert blocked_response.status_code == 429


## 2. Test: /submit enforces rate limit and returns 429 when exceeded
def test_submit_rate_limit_enforced(client: TestClient):
    app.dependency_overrides[get_current_user] = mock_normal_user
    submit_payload = {"challenge_id": 1, "flag_input": "FLAG{test_guess}"}

    # First 2 requests are within the "2/minute" limit
    for _ in range(2):
        response = client.post("/api/v1/game/submit", json=submit_payload)
        assert response.status_code != 429

    # 3rd request exceeds "2/minute" -> 429 Too Many Requests
    blocked_response = client.post("/api/v1/game/submit", json=submit_payload)
    assert blocked_response.status_code == 429


## 3. Test: Admin can disable rate limiting via PUT /settings/rate_limit
def test_admin_can_disable_rate_limit(client: TestClient):
    app.dependency_overrides[get_current_admin_user := get_current_user] = mock_admin_user

    # Disable rate limiting via the admin endpoint
    toggle_payload = {
        "rate_limit_enabled": False,
        "login_rate_limit": "2/minute",
        "submit_rate_limit": "2/minute",
    }
    update_res = client.put("/api/v1/admin/settings/rate_limit", json=toggle_payload)
    assert update_res.status_code == 200
    assert update_res.json()["rate_limit_enabled"] is False

    # Send 5 rapid requests to /submit (well above "2/minute") -> none should return 429
    app.dependency_overrides[get_current_user] = mock_normal_user
    submit_payload = {"challenge_id": 1, "flag_input": "FLAG{test_guess}"}
    for _ in range(5):
        response = client.post("/api/v1/game/submit", json=submit_payload)
        assert response.status_code != 429


## 4. Test: Admin can configure custom non-default rate limits
def test_admin_can_configure_custom_rate_limit(client: TestClient):
    app.dependency_overrides[get_current_user] = mock_admin_user

    # Increase /login limit from "3/minute" to "5/minute"
    custom_payload = {
        "rate_limit_enabled": True,
        "login_rate_limit": "5/minute",
        "submit_rate_limit": "10/minute",
    }
    update_res = client.put("/api/v1/admin/settings/rate_limit", json=custom_payload)
    assert update_res.status_code == 200
    assert update_res.json()["login_rate_limit"] == "5/minute"

    # Now 5 login attempts should succeed without 429, and the 6th should trigger 429
    login_payload = {"username": "nonexistent", "password": "wrongpassword"}
    for _ in range(5):
        res = client.post("/api/v1/auth/login", data=login_payload)
        assert res.status_code != 429

    blocked_res = client.post("/api/v1/auth/login", data=login_payload)
    assert blocked_res.status_code == 429


## 5. Test: Regular player cannot modify rate limit settings (RBAC check)
def test_player_cannot_modify_rate_limit(client: TestClient):
    app.dependency_overrides[get_current_user] = mock_normal_user

    payload = {
        "rate_limit_enabled": False,
        "login_rate_limit": "100/minute",
        "submit_rate_limit": "100/minute",
    }
    response = client.put("/api/v1/admin/settings/rate_limit", json=payload)
    assert response.status_code == 403
