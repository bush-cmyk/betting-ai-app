from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import joblib
import numpy as np

OUTCOMES = ["AWAY", "DRAW", "HOME"]

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL_PATH = REPO_ROOT / "ai" / "artifacts" / "sports_model.joblib"


class SportsPredictor:
    def __init__(self, model_path: Path = DEFAULT_MODEL_PATH) -> None:
        self.model_path = model_path
        self.model = None

        if self.model_path.exists():
            self.model = joblib.load(self.model_path)

    @staticmethod
    def _features(
        home_form: float,
        away_form: float,
        home_strength: float,
        away_strength: float,
        home_advantage: bool,
    ) -> np.ndarray:
        return np.array(
            [
                [
                    home_form,
                    away_form,
                    home_strength,
                    away_strength,
                    1.0 if home_advantage else 0.0,
                ]
            ],
            dtype=float,
        )

    @staticmethod
    def _fallback_probabilities(
        home_form: float,
        away_form: float,
        home_strength: float,
        away_strength: float,
        home_advantage: bool,
    ) -> Dict[str, float]:
        strength_delta = (home_strength - away_strength) / 100.0
        form_delta = home_form - away_form
        advantage = 0.08 if home_advantage else 0.0

        home_signal = 0.5 + (0.42 * strength_delta) + (0.32 * form_delta) + advantage
        home_signal = float(np.clip(home_signal, 0.08, 0.88))

        draw_signal = 0.28 - (0.22 * abs(strength_delta)) - (0.16 * abs(form_delta))
        draw_signal = float(np.clip(draw_signal, 0.08, 0.30))

        away_signal = max(0.05, 1.0 - home_signal - draw_signal)

        raw = np.array([away_signal, draw_signal, home_signal], dtype=float)
        raw = raw / raw.sum()

        return {
            "AWAY": float(raw[0]),
            "DRAW": float(raw[1]),
            "HOME": float(raw[2]),
        }

    def predict(
        self,
        home_form: float,
        away_form: float,
        home_strength: float,
        away_strength: float,
        home_advantage: bool,
    ) -> Tuple[str, float, Dict[str, float], str]:
        if self.model is None:
            probabilities = self._fallback_probabilities(
                home_form,
                away_form,
                home_strength,
                away_strength,
                home_advantage,
            )
            outcome = max(probabilities, key=probabilities.get)
            confidence = probabilities[outcome]
            return outcome, confidence, probabilities, "fallback_demo"

        features = self._features(
            home_form,
            away_form,
            home_strength,
            away_strength,
            home_advantage,
        )

        predicted = str(self.model.predict(features)[0])
        probability_values = self.model.predict_proba(features)[0]

        probabilities = {
            str(label): float(probability)
            for label, probability in zip(self.model.classes_, probability_values)
        }

        # Keep a stable client contract even if class order changes.
        probabilities = {
            outcome: probabilities.get(outcome, 0.0)
            for outcome in ["HOME", "DRAW", "AWAY"]
        }

        confidence = max(probabilities.values())
        return predicted, confidence, probabilities, "trained_model"
