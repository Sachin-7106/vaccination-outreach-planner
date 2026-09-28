# Automated Testing Specification

This document details the unit, integration, API, database, and failure scenario testing strategy for the **City Health Vaccination Outreach Planner**.

---

## 🎯 Testing Strategy & Architecture

The testing suite uses **Pytest** with an isolated in-memory SQLite database environment (`StaticPool` connection pool) to guarantee idempotent, zero-side-effect execution across test runs.

```
                  ┌──────────────────────────────┐
                  │        Pytest Runner         │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Unit Tests     │    │  Integration &   │    │ Database & Data  │
│(Scoring, Limits, │    │    API Tests     │    │ Integrity Tests  │
│  Evaluator KPIs) │    │(FastAPI Client)  │    │ (ORM & Pydantic) │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## 📋 Test Suite Organization & Coverage Matrix

| Test Module | Purpose | Validated Functionality & Coverage | Number of Tests |
|---|---|---|---|
| **`tests/test_scoring.py`** | Multi-Objective Scoring Engines | Tests Baseline, Maximum Reach, and Emerging Risk Reduction engines. Validates min-max score normalization [0.0, 1.0], priority ranking, ties, and custom weighting factors. | **5 tests** |
| **`tests/test_constraints.py`** | Hard & Soft Operational Boundaries | Tests travel distance limit enforcing (`max_travel_distance_km`), session supply capacity scaling, low accessibility warnings, high mobility transit flags, and low historical attendance advisories. | **6 tests** |
| **`tests/test_audit_flow.py`** | Human Review Governance & Audit | Validates override justification requirement (min 5 characters), HTTP 400 error handling on missing justification, successful override submission, and audit trail persistence. | **1 test** |
| **`tests/test_evaluator.py`** | KPI & Evaluation Metrics Engine | Validates total eligible reached, total capacity allocated, session utilization rate, unmet demand, risk-weighted coverage score, travel feasibility rate, and empty input handling. | **3 tests** |
| **`tests/test_api.py`** | FastAPI REST API Router Integration | End-to-end HTTP integration tests using `TestClient`. Tests `/`, `/api/areas`, `/api/areas/{id}`, `/api/planner/generate`, `/api/planner/compare`, `/api/eval/metrics`, `/api/eval/error-analysis`, and HTTP 422 input validation errors. | **10 tests** |
| **`tests/test_reviews.py`** | Review Decision Workflows & Filtering | Tests `ACCEPTED`, `MODIFIED`, `REJECTED`, and `OVERRIDDEN` decision statuses, modified capacity updates, audit trail log fetching ordered by timestamp desc, and recommendation status filtering. | **5 tests** |
| **`tests/test_error_cases.py`** | Algorithmic Failure Mode Scenarios | Tests all 4 failure scenarios (`ERR-01` to `ERR-04`), capacity bottlenecks, access barriers, historical lag overrides, resource competition tie-breakers, and empty area input arrays. | **5 tests** |
| **`tests/test_data_integrity.py`** | Database Schema & Pydantic Schema | Tests SQLAlchemy ORM relationships, foreign key back-populates (`Area` -> `ServiceHistory`, `DiseaseRisk`, `MobilityPattern`), and Pydantic parameter boundary validation rules. | **3 tests** |

**Total Test Count**: **38 Automated Tests (100% Passing)**

---

## 🚀 How to Run the Test Suite

### Command Execution
Set `PYTHONPATH` to include the `backend/` directory and execute `pytest`:

```powershell
$env:PYTHONPATH="backend"
python -m pytest tests/ -v
```

### Expected Output
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
collected 38 items

tests/test_api.py::test_root_endpoint PASSED                             [  2%]
tests/test_api.py::test_list_areas_api PASSED                            [  5%]
...
tests/test_scoring.py::test_custom_weighting_parameters PASSED           [100%]

======================= 38 passed, 4 warnings in 0.77s ========================
```
