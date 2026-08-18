from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import PredictionRequest, PredictionResponse
from app.services.predictor import SportsPredictor

app = FastAPI(
    title="SportsAI Simulation API",
    version="0.1.0",
    description=(
        "Educational sports-outcome simulation API. "
        "This service does not place wagers or provide betting advice."
    ),
)

# Development-only CORS setting. Restrict origins before production deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

predictor = SportsPredictor()

DISCLAIMER = (
    "Educational simulation only. This output is not financial or betting advice "
    "and is not intended for real-money wagering."
)


@app.get("/")
def root():
    return {
        "name": "SportsAI Simulation API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": predictor.model is not None,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    outcome, confidence, probabilities, model_source = predictor.predict(
        home_form=payload.home_form,
        away_form=payload.away_form,
        home_strength=payload.home_strength,
        away_strength=payload.away_strength,
        home_advantage=payload.home_advantage,
    )

    return PredictionResponse(
        predicted_outcome=outcome,
        confidence=round(confidence, 4),
        probabilities={
            key: round(value, 4) for key, value in probabilities.items()
        },
        model_source=model_source,
        disclaimer=DISCLAIMER,
    )
