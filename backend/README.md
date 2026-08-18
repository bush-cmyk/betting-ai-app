# Backend

FastAPI service for validating input and serving sports outcome simulations.

## Install

From the repository root:

```bash
pip install -r backend/requirements.txt
```

## Run

```bash
cd backend
uvicorn app.main:app --reload
```

Endpoints:

- `GET /`
- `GET /health`
- `POST /predict`
- `GET /docs` — interactive OpenAPI documentation

The backend looks for a trained model at:

```text
../ai/artifacts/sports_model.joblib
```

If no model exists, it uses a transparent fallback scoring function so the API remains runnable.
