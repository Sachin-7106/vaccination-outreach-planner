# City Health Department — Seasonal Infectious Disease Vaccination Outreach Planner

> **Review #2 Milestone (70%+ Overall Project Completion)**  
> *A human-in-the-loop decision support system for planning seasonal vaccination outreach using aggregate non-discriminatory population risk indicators.*

---

## 🌟 Project Overview

The **City Health Vaccination Outreach Planner** addresses a critical operational challenge in public health resource allocation: **legacy allocation policies relying purely on historical session attendance miss sudden, localized infectious disease outbreaks in vulnerable, under-served, and highly mobile urban populations.**

This decision support platform equips public health directors, clinical reviewers, and field outreach coordinators with data-driven, 100% explainable multi-objective optimization to dynamically deploy mobile vaccination clinics where disease transmission risk is highest.

---

## 🏛️ Architecture Summary

The application follows a clean, decoupled 3-tier architecture:

```
┌─────────────────────────────────────────────────────────┐
│              React 18 + Vite Frontend                   │
│   (Dashboard, Area Explorer, Planner, Review Console,   │
│         Evaluation KPIs, Interactive Leaflet Maps)      │
└────────────────────────────┬────────────────────────────┘
                             │ REST API (JSON)
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                        │
│   (Pydantic Validation, FastAPI Routers, NumPy Scoring  │
│      Engines, Constraint Checker, Explainability)       │
└────────────────────────────┬────────────────────────────┘
                             │ SQLAlchemy ORM
                             ▼
┌─────────────────────────────────────────────────────────┐
│               SQLite Relational Database                │
│    (12 City Zones, Service Histories, Risk Signals,     │
│   Mobility Corridors, Recommendations, Audit Trail)     │
└─────────────────────────────────────────────────────────┘
```

---

## ⚡ Core Features

1. **Surveillance & Area Explorer**: Interactive Leaflet map visualizing 12 synthetic city zones with demographic, coverage, and emerging disease risk indicators.
2. **Multi-Objective Optimization Engines**:
   - **Objective A (Maximum Eligible Reach)**: Focuses on large unvaccinated population pools and road accessibility.
   - **Objective B (Emerging Risk Reduction - Proposed)**: Prioritizes disease velocity spikes, unvaccinated gaps, transit mobility, and population scale.
   - **Historical Average Baseline**: Benchmark model demonstrating how legacy historical planning misses outbreak spikes.
3. **Hard & Soft Operational Constraint Engine**: Enforces travel distance limits (`max_travel_distance_km`), scales expected reach to remaining unvaccinated pools, and flags low accessibility zones or high mobility corridors.
4. **100% Explainable Recommendations**: Provides structured, human-readable factor score breakdowns explaining why each zone was prioritized.
5. **Human Review & Immutable Audit Trail Console**: Authorized clinicians can `ACCEPT`, `MODIFY`, `REJECT`, or `OVERRIDE` recommendations. Overriding hard constraints mandates a documented justification string logged permanently for audit compliance.
6. **Empirical Performance & KPI Evaluation**: Interactive Recharts matrix measuring total eligible reached, supply capacity utilization, unmet demand, risk-weighted coverage, and travel feasibility rates across objectives.
7. **Failure Analysis & Error Boundaries**: Detailed documentation and automated test coverage for 4 real-world algorithmic failure modes (`ERR-01` to `ERR-04`).

---

## 🗄️ Database Overview

The system uses a relational SQLite database schema managed via SQLAlchemy ORM.

### Major Entities & Relationships:
- **`areas`** $\rightarrow$ Primary entity representing 12 synthetic city zones with geographic coordinates, population, and accessibility indices.
- **`service_history`** $\rightarrow$ Tracks past outreach session attendance, service visits, and historical demand.
- **`disease_risk`** $\rightarrow$ Stores baseline seasonal risk and emerging outbreak risk velocity signals.
- **`mobility_patterns`** $\rightarrow$ Monitors population movement indices, daytime transit influx, and commuter efflux.
- **`outreach_sessions`** $\rightarrow$ Records completed and scheduled mobile outreach session deployments.
- **`recommendations`** $\rightarrow$ System-generated priority recommendations with normalized scores, ranks, and constraint flags.
- **`reviews`** $\rightarrow$ Immutable governance audit log storing reviewer decisions, timestamps, and mandatory justification override statements.

For detailed table definitions and Mermaid ER diagrams, see [data-schema.md](file:///c:/city%20health/docs/data-schema.md).

---

## 📚 Technical Documentation

Explore detailed technical documentation in the `docs/` directory:

- 🏛️ [Architecture Specification](file:///c:/city%20health/docs/architecture.md)
- 🗄️ [Database Schema Specification](file:///c:/city%20health/docs/data-schema.md)
- 🌐 [REST API Specification](file:///c:/city%20health/docs/api-spec.md)
- 🧪 [Automated Testing Documentation](file:///c:/city%20health/docs/testing.md)
- 🛡️ [Error Boundaries & Propagation Specification](file:///c:/city%20health/docs/error-boundaries.md)
- ⚠️ [Failure Analysis & Algorithmic Scenarios](file:///c:/city%20health/docs/failure-scenarios.md)
- 📋 [Risk Register](file:///c:/city%20health/docs/risk-register.md)
- 👤 [User Journeys Specification](file:///c:/city%20health/docs/user-journeys.md)
- 🎯 [Problem Validation & Requirements](file:///c:/city%20health/docs/problem-validation.md)

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Leaflet / React-Leaflet, Recharts, Lucide React, Vanilla CSS Design System Tokens.
- **Backend**: Python 3.11, FastAPI, Uvicorn, NumPy, Pydantic V2.
- **Database**: SQLite 3, SQLAlchemy 2.0 ORM.
- **Testing & Tooling**: Pytest, FastAPI TestClient, SQLite StaticPool.

---

## 🚀 How to Run the Application

### Prerequisites
- Python 3.10+
- Node.js v18+ and npm

### Quick Start (Windows)
Double-click `run_app.bat` or run in PowerShell:
```powershell
.\run_app.bat
```

### Manual Launch

#### 1. Start FastAPI Backend Server
```powershell
# Set PYTHONPATH to backend directory
$env:PYTHONPATH="backend"
python backend/main.py
```
*Backend API runs at: `http://127.0.0.1:8000`*  
*Swagger API Docs at: `http://127.0.0.1:8000/docs`*

#### 2. Start React + Vite Frontend Dev Server
```powershell
cd frontend
npm install
npm run dev
```
*Frontend runs at: `http://localhost:3000`*

---

## 🧪 Testing & Performance Validation

### Running Automated Test Suite
The repository includes 38 automated test cases across 8 test modules:

```powershell
$env:PYTHONPATH="backend"
python -m pytest tests/ -v
```

### Running Performance Benchmark
Measure execution time for scoring engines and constraint evaluation over 1,000 iterations:

```powershell
$env:PYTHONPATH="backend"
python scripts/benchmark_planner.py
```

*Measured Performance*:
- **Historical Baseline**: ~0.0468 ms avg per execution
- **Maximum Reach Engine**: ~0.1053 ms avg per execution
- **Emerging Risk Reduction Engine**: ~0.1361 ms avg per execution

---

## 📈 Project Milestone Status (Review #2 — 70% Milestone)

| Milestone Category | Progress | Status |
|---|---|---|
| **Core Architecture & Frontend UI** | Working React + Vite frontend, interactive Leaflet map, dashboard metrics | **Completed** |
| **Backend REST API** | FastAPI routers for areas, planner, reviews, and evaluation metrics | **Completed** |
| **Relational Database** | SQLite schema with 7 entities, foreign keys, and seed data builder | **Completed** |
| **Multi-Objective Optimization** | Vectorized NumPy scoring engines for Baseline, Reach, and Risk Reduction | **Completed** |
| **Constraint Engine** | Hard travel limits, supply capacity scaling, and soft accessibility/mobility flags | **Completed** |
| **Governance & Audit Trail** | Mandatory human review justification for constraint overrides logged to DB | **Completed** |
| **Technical Documentation** | Granular API spec, Error boundaries, Database schema, Testing doc, Failure scenarios | **Completed** |
| **Automated Testing** | 38 granular Pytest unit & API test cases covering 100% of modules | **Completed** |
| **Future Work (Final 30%)** | Real-time GIS feeds, multi-period demand forecasting, RBAC auth, production deployment | *Planned for Final Review* |
