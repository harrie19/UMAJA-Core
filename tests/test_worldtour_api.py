import importlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_DIR = PROJECT_ROOT / "api"

if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))


def _get_client(monkeypatch, tmp_path):
    db_path = tmp_path / "worldtour_cities.json"
    votes_path = tmp_path / "worldtour_votes.json"

    monkeypatch.setenv("WORLDTOUR_DB_PATH", str(db_path))
    monkeypatch.setenv("WORLDTOUR_VOTES_PATH", str(votes_path))

    import simple_server

    simple_server = importlib.reload(simple_server)
    return simple_server.app.test_client()


def test_worldtour_start_endpoint(monkeypatch, tmp_path):
    client = _get_client(monkeypatch, tmp_path)

    response = client.post("/api/worldtour/start")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["success"] is True
    assert payload["content"]["city_id"] == payload["city_id"]
    assert payload["stats"]["visited_cities"] >= 1


def test_worldtour_cities_and_vote(monkeypatch, tmp_path):
    client = _get_client(monkeypatch, tmp_path)

    cities_response = client.get("/api/worldtour/cities")
    assert cities_response.status_code == 200

    cities_payload = cities_response.get_json()
    assert cities_payload["cities"]

    city_id = cities_payload["cities"][0]["id"]

    vote_response = client.post("/api/worldtour/vote", json={"city_id": city_id})
    assert vote_response.status_code == 200

    analytics_response = client.get("/api/analytics/worldtour")
    assert analytics_response.status_code == 200

    analytics_payload = analytics_response.get_json()
    assert "total_cities" in analytics_payload
    assert "visited_cities" in analytics_payload
