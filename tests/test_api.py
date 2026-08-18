import sys
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_valid_request():
    response = client.post(
        "/predict",
        json={
            "home_form": 0.80,
            "away_form": 0.55,
            "home_strength": 84,
            "away_strength": 77,
            "home_advantage": True,
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["predicted_outcome"] in {"HOME", "DRAW", "AWAY"}
    assert 0 <= body["confidence"] <= 1

    total = sum(body["probabilities"].values())
    assert abs(total - 1.0) < 0.02


def test_predict_rejects_invalid_form():
    response = client.post(
        "/predict",
        json={
            "home_form": 1.25,
            "away_form": 0.55,
            "home_strength": 84,
            "away_strength": 77,
            "home_advantage": True,
        },
    )

    assert response.status_code == 422
