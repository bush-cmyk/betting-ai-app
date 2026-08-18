from typing import Dict, Literal

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    home_form: float = Field(
        ge=0.0,
        le=1.0,
        description="Recent home-team form expressed from 0 to 1.",
    )
    away_form: float = Field(
        ge=0.0,
        le=1.0,
        description="Recent away-team form expressed from 0 to 1.",
    )
    home_strength: float = Field(
        ge=0.0,
        le=100.0,
        description="Demo home-team strength rating.",
    )
    away_strength: float = Field(
        ge=0.0,
        le=100.0,
        description="Demo away-team strength rating.",
    )
    home_advantage: bool = Field(
        default=True,
        description="Whether the home side receives the demo home-advantage factor.",
    )


class PredictionResponse(BaseModel):
    predicted_outcome: Literal["HOME", "DRAW", "AWAY"]
    confidence: float
    probabilities: Dict[str, float]
    model_source: str
    disclaimer: str
