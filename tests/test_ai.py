import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.predictor import SportsPredictor  # noqa: E402


def test_fallback_probabilities_sum_to_one():
    probabilities = SportsPredictor._fallback_probabilities(
        home_form=0.75,
        away_form=0.40,
        home_strength=82,
        away_strength=70,
        home_advantage=True,
    )

    assert set(probabilities) == {"HOME", "DRAW", "AWAY"}
    assert abs(sum(probabilities.values()) - 1.0) < 1e-9


def test_fallback_prefers_stronger_home_team():
    probabilities = SportsPredictor._fallback_probabilities(
        home_form=0.90,
        away_form=0.20,
        home_strength=92,
        away_strength=55,
        home_advantage=True,
    )

    assert probabilities["HOME"] > probabilities["AWAY"]
