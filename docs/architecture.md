# System Architecture

## Overview

SportsAI Sim uses a simple three-layer architecture:

```text
┌──────────────────────────────┐
│ Mobile Client                │
│ Expo / React Native          │
└──────────────┬───────────────┘
               │ HTTPS / JSON
               ▼
┌──────────────────────────────┐
│ Backend API                  │
│ FastAPI + Pydantic           │
└──────────────┬───────────────┘
               │ validated features
               ▼
┌──────────────────────────────┐
│ AI Prediction Service        │
│ scikit-learn model           │
└──────────────┬───────────────┘
               │
               ▼
       outcome probabilities
```

## Mobile Layer

Responsibilities:

- collect simulation inputs
- validate basic user input
- call the backend API
- display outcome probabilities
- show simulation disclaimer

## Backend Layer

Responsibilities:

- expose REST endpoints
- validate request data
- isolate model execution from the client
- return a stable JSON response
- provide OpenAPI documentation

## AI Layer

Responsibilities:

- create a reproducible demonstration dataset
- train a multiclass model
- persist the model artifact
- return probabilities for `HOME`, `DRAW`, and `AWAY`

## Current Limitation

The current model is trained on synthetic data and must not be interpreted as evidence of real-world predictive accuracy.
