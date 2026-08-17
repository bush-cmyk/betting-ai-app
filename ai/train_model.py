from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_SEED = 42
OUTPUT_PATH = Path(__file__).resolve().parent / "artifacts" / "sports_model.joblib"


def generate_synthetic_data(rows: int = 4000):
    rng = np.random.default_rng(RANDOM_SEED)

    home_form = rng.uniform(0, 1, rows)
    away_form = rng.uniform(0, 1, rows)
    home_strength = rng.uniform(35, 95, rows)
    away_strength = rng.uniform(35, 95, rows)
    home_advantage = rng.integers(0, 2, rows)

    score = (
        1.7 * (home_form - away_form)
        + 0.045 * (home_strength - away_strength)
        + 0.40 * home_advantage
        + rng.normal(0, 0.75, rows)
    )

    y = np.where(score > 0.55, "HOME", np.where(score < -0.55, "AWAY", "DRAW"))

    X = np.column_stack(
        [
            home_form,
            away_form,
            home_strength,
            away_strength,
            home_advantage,
        ]
    )

    return X, y


def main():
    X, y = generate_synthetic_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    model = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print(f"Holdout accuracy on synthetic data: {accuracy:.3f}")
    print(classification_report(y_test, predictions))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUTPUT_PATH)
    print(f"Saved model to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
