# Error Boundaries Specification

This document details how operational errors, validation failures, constraint violations, and system exceptions propagate through the **City Health Vaccination Outreach Planner** architecture.

---

## 🏗️ End-to-End Error Flow Architecture

```
[ Frontend User Input ]
          │
          ▼
[ API Request Validation (Pydantic / FastAPI) ]
          │
          ▼
[ Business Logic & Database Queries (SQLAlchemy) ]
          │
          ▼
[ Planner / Scoring Engines (NumPy Vectorized) ]
          │
          ▼
[ Operational Constraint Evaluator (Hard & Soft Rules) ]
          │
          ▼
[ Database Persistence (SQLite Session) ]
          │
          ▼
[ API HTTP Response Payload (Status Code & JSON Detail) ]
          │
          ▼
[ Frontend State & UI Error Alerts (Toast / Banner) ]
```

---

## 🛡️ Detailed Error Categories & Boundaries

### 1. Invalid Request Input & Parameter Out of Bounds

- **Origin**: Frontend user inputs in Outreach Planner UI (e.g. session count set to 0 or 100, negative capacity).
- **Detection**: FastAPI request layer via Pydantic model validation schema (`PlanRequest` in `backend/app/models/pydantic_models.py`).
- **Handling**: Pydantic intercepts parameter values before reaching endpoint handler logic.
- **API Response**: `HTTP 422 Unprocessable Entity` with JSON validation detail specifying field path and constraint (e.g., `num_sessions ge 1`).
- **Frontend Behavior**: `api.js` Axios client catches HTTP 422 errors; UI components display field-level validation messages or toast notifications preventing form submission.

---

### 2. Missing Resource / Entity Not Found

- **Origin**: Requesting details for a non-existent area ID (e.g., `GET /api/areas/AREA-999`) or non-existent recommendation ID during human review (`POST /api/reviews/approve`).
- **Detection**: SQLAlchemy ORM query returns `None` during database lookup in API router handlers (`backend/app/api/areas.py`, `backend/app/api/reviews.py`).
- **Handling**: Router code explicitly checks entity existence and raises `fastapi.HTTPException(status_code=404, detail="Area not found")`.
- **API Response**: `HTTP 404 Not Found` with JSON detail message (`{"detail": "Recommendation not found"}`).
- **Frontend Behavior**: Frontend displays a "Resource Not Found" placeholder screen or alerts the user with an actionable back-to-dashboard navigation button.

---

### 3. Missing Human Review Justification (Override Boundary)

- **Origin**: Review console attempt to override a hard constraint without entering a documented justification reason.
- **Detection**: Review router logic (`backend/app/api/reviews.py`) checking `if req.decision == "OVERRIDDEN" and (not req.override_reason or len(req.override_reason.strip()) < 5)`.
- **Handling**: Exception handler blocks state change and raises `fastapi.HTTPException(status_code=400, detail="Overriding a hard constraint requires a documented justification reason (min 5 characters).")`.
- **API Response**: `HTTP 400 Bad Request`.
- **Frontend Behavior**: `HumanReviewModal.jsx` highlights the justification text field in red, displays an error warning message, and keeps the modal open until the user provides a valid reason.

---

### 4. Operational Hard Constraint Failure

- **Origin**: Scoring engines select a high-priority area whose distance from base exceeds the fleet maximum radius (e.g. `AREA-09` distance `16.5 km > 12.0 km`).
- **Detection**: Evaluated by `evaluate_constraints()` in `backend/app/planner/constraints.py`.
- **Handling**: Sets `hard_constraint_passed = False`, attaches structured flag `HARD_TRAVEL_EXCEEDED`, and flags status as `PENDING` human review.
- **API Response**: `HTTP 200 OK` (successful recommendation generation) with `hard_constraint_passed: false` and explicit `constraint_flags` payload.
- **Frontend Behavior**: `RecommendationCard.jsx` and `ReviewConsole.jsx` render red warning badges ("HARD CONSTRAINT VIOLATION"), disabling auto-approval and requiring explicit clinician override.

---

### 5. Supply Capacity Scaling (Soft Constraint Boundary)

- **Origin**: Selected zone's remaining unvaccinated pool is smaller than single session supply capacity (e.g. 100 unvaccinated vs 300 session capacity).
- **Detection**: Evaluated in `backend/app/planner/constraints.py` (`expected_reach = min(unvaccinated, session_capacity)`).
- **Handling**: Automatically scales down `expected_reach` to avoid artificial vaccine wastage and appends `SOFT_LIMITED_UNVACCINATED_POOL` warning.
- **API Response**: Returns modified `expected_reach` integer and soft constraint warning list.
- **Frontend Behavior**: Displays yellow advisory badge explaining supply scaling without blocking plan acceptance.

---

### 6. Database Schema & Integrity Constraint Exceptions

- **Origin**: Concurrent database writes, SQLite lock contention, or foreign key constraint violations.
- **Detection**: Caught by SQLAlchemy `IntegrityError` or `OperationalError` during `db.commit()`.
- **Handling**: Endpoint wrapped in database session try/except block; `db.rollback()` executes, reverting uncommitted transactions before re-raising formatted error.
- **API Response**: `HTTP 500 Internal Server Error` with sanitized error log description.
- **Frontend Behavior**: Axios interceptor catches 500 status code and renders a retry prompt to prevent inconsistent local state.

---

## 📋 Error Response Matrix Summary

| Error Category | Source File | HTTP Code | Mitigation Strategy | Frontend UI Behavior |
|---|---|---|---|---|
| **Input Out of Bounds** | `models/pydantic_models.py` | `422` | Schema bounds enforcement | Inline input field warning |
| **Missing Resource** | `api/areas.py`, `api/reviews.py` | `404` | Explicit entity lookup check | Not Found state screen |
| **Missing Override Justification** | `api/reviews.py` | `400` | Mandatory string validation | Red field border & alert |
| **Hard Travel Exceeded** | `planner/constraints.py` | `200` | `hard_constraint_passed=False` | Red badge & Human Override required |
| **Capacity Pool Deficit** | `planner/constraints.py` | `200` | Capped `expected_reach` | Yellow advisory badge |
| **Database Transaction Failure** | `core/database.py` | `500` | Transaction rollback | System error toast & retry button |
