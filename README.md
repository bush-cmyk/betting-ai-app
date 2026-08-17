# Betting AI App

A portfolio-ready **sports outcome simulation** project that demonstrates mobile development, API design, machine learning, testing, documentation, and secure software practices.

> **Important:** This project is for education and simulation only. It does not place real-money wagers and should not be treated as financial or betting advice.

## Architecture

```text
Mobile App (Expo / React Native)
        |
        | HTTP / JSON
        v
FastAPI Backend
        |
        | feature vector
        v
AI Prediction Layer
        |
        v
Prediction + probabilities
```

## Repository Structure

```text
betting-ai-app/
├── mobile/      # Expo / React Native client
├── backend/     # FastAPI service
├── ai/          # ML training and model utilities
├── docs/        # Architecture, API, security, and project notes
└── tests/       # Automated tests
```

## Quick Start

### 1. Create and activate a Python environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install backend and AI dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Train the demo model

```bash
python ai/train_model.py
```

This creates:

```text
ai/artifacts/sports_model.joblib
```

### 4. Start the backend

```bash
cd backend
uvicorn app.main:app --reload
```

API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

### 5. Start the mobile app

In another terminal:

```bash
cd mobile
npm install
npx expo start
```

For a physical phone, copy `.env.example` to `.env` and replace the API address with your computer's LAN IP.

## Example Prediction Request

```json
{
  "home_form": 0.80,
  "away_form": 0.55,
  "home_strength": 84,
  "away_strength": 77,
  "home_advantage": true
}
```

## Portfolio Skills Demonstrated

- Python
- FastAPI
- REST API design
- React Native / Expo
- Machine learning with scikit-learn
- Git and GitHub
- Automated testing with pytest
- API validation
- Secure configuration practices
- Technical documentation

## Roadmap

- [x] Repository architecture
- [x] Prediction API
- [x] Demo ML training pipeline
- [x] Mobile prediction screen
- [x] Automated API and AI tests
- [ ] User authentication
- [ ] Sports data provider integration
- [ ] Prediction history
- [ ] Database persistence
- [ ] Model monitoring
- [ ] CI/CD workflow
