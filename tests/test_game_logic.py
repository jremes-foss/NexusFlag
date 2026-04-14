from app.api.deps import get_current_user
from app.main import app
from tests.factories import UserFactory, ChallengeFactory

def test_first_blood_bonus_with_factories(client):
    challenge = ChallengeFactory(points=200, flag="CTF{win}")
    user_a = UserFactory()
    user_b = UserFactory()

    app.dependency_overrides[get_current_user] = lambda: user_a
    
    response_a = client.post(
        "/api/v1/game/submit",
        json={"challenge_id": challenge.id, "flag_input": "CTF{win}"}
    )
    
    assert response_a.status_code == 200
    assert response_a.json()["new_score"] == 220

    app.dependency_overrides[get_current_user] = lambda: user_b
    
    response_b = client.post(
        "/api/v1/game/submit",
        json={"challenge_id": challenge.id, "flag_input": "CTF{win}"}
    )
    
    assert response_b.status_code == 200
    assert response_b.json()["new_score"] == 200

    app.dependency_overrides.clear()
