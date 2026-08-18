# API

Base development URL:

```text
http://127.0.0.1:8000
```

## GET `/health`

Response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

## POST `/predict`

Request:

```json
{
  "home_form": 0.8,
  "away_form": 0.55,
  "home_strength": 84,
  "away_strength": 77,
  "home_advantage": true
}
```

Validation:

- `home_form`: 0–1
- `away_form`: 0–1
- `home_strength`: 0–100
- `away_strength`: 0–100
- `home_advantage`: boolean

Response:

```json
{
  "predicted_outcome": "HOME",
  "confidence": 0.6214,
  "probabilities": {
    "HOME": 0.6214,
    "DRAW": 0.2102,
    "AWAY": 0.1684
  },
  "model_source": "trained_model",
  "disclaimer": "Educational simulation only..."
}
```
