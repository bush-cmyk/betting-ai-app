# Security Notes

## Current MVP

This repository is a demonstration project and does not process money, wagers, payment cards, or government-issued identity documents.

## Practices Included

- Server-side request validation with Pydantic.
- Model execution remains on the backend.
- API endpoint is configurable from the mobile client.
- No API keys are committed to source control.
- Development CORS behavior is clearly marked.
- Public client environment variables are treated as non-secret.

## Before Production

A production deployment should add:

1. HTTPS everywhere.
2. Strict CORS allowlists.
3. Authentication and authorization.
4. Rate limiting.
5. Centralized secret management.
6. Structured logging without sensitive data.
7. Dependency and container vulnerability scanning.
8. Abuse detection.
9. Database encryption and secure backups.
10. Applicable age, gaming, privacy, and jurisdiction controls if real wagering is ever introduced.

## Model Artifact Safety

Serialized Python model files should only be loaded from trusted sources. Do not load arbitrary or user-uploaded model artifacts.
