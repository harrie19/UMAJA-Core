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

    response = client.post("/worldtour/start")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["success"] is True
    assert "next_city" in payload
    assert payload["stats"]["visited_cities"] >= 0


def test_worldtour_cities_and_status(monkeypatch, tmp_path):
    client = _get_client(monkeypatch, tmp_path)

    cities_response = client.get("/worldtour/cities")
    assert cities_response.status_code == 200

    cities_payload = cities_response.get_json()
    assert cities_payload["success"] is True
    assert cities_payload["cities"]

    city_id = cities_payload["cities"][0]["id"]

    status_response = client.get("/worldtour/status")
    assert status_response.status_code == 200

    status_payload = status_response.get_json()
    assert "stats" in status_payload
    assert "status" in status_payload
