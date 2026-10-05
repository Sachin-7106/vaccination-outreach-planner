# Deployment & Production Hardening Guide

## Overview
This document outlines production deployment procedures, environment configuration, database management, and operational hardening for the City Health Vaccination Outreach Planner.

---

## 1. Environment Configuration

All operational parameters are configured via environment variables. Create a `.env` file in the project root based on `.env.example`:

```env
# Application Settings
PROJECT_NAME="Vaccination Outreach Planner"
ENVIRONMENT="production"
DATABASE_URL="sqlite:///./city_health.db"

# Security & Authentication
JWT_SECRET="generate_a_secure_64_byte_random_string_here"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Hardened CORS Origins (Comma-separated)
CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173,https://outreach.cityhealth.gov"
```

---

## 2. Backend Service Deployment

### Prerequisites
- Python 3.11+
- COIN-OR CBC Solver (installed automatically via `pulp` wheel or system package)

### Installation & Run

```bash
# Set PYTHONPATH to include backend directory
$env:PYTHONPATH="backend"

# Run database initialization & seed
python backend/app/data/seed_data.py

# Launch production server with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 3. Health & Readiness Monitoring

The application provides standardized liveness and readiness probe endpoints for orchestrators (e.g. Kubernetes, Docker Healthchecks):

- **Liveness Probe**: `GET /health` (Returns HTTP 200 `{"status": "UP"}`)
- **Readiness Probe**: `GET /readiness` (Verifies SQLite/PostgreSQL connection, returns HTTP 200 `{"status": "READY"}` or HTTP 503 if database unreachable).

---

## 4. Frontend Production Build & Deployment

```bash
cd frontend
npm install
npm run build
```

The production-ready static assets will be output to `frontend/dist/`. Serve `frontend/dist` using Nginx, Caddy, or a CDN with HTTP/2 and TLS enabled.

---

## 5. Security & Hardening Checklist

- [x] Configure explicit non-wildcard `CORS_ORIGINS`.
- [x] Use salted PBKDF2-SHA256 password hashing.
- [x] Rotate JWT secrets in production environment.
- [x] Use atomic state transitions for recommendation review status.
- [x] Protect API endpoints with backend-enforced RBAC (`ADMIN` vs `CLINICIAN`).
