# REST API Specification

This document details every REST endpoint provided by the **FastAPI Backend** of the City Health Vaccination Outreach Planner.

OpenAPI / Swagger interactive documentation is generated automatically by FastAPI at:  
`http://127.0.0.1:8000/docs`

---

## 🌐 System Endpoints

### 1. Service Health Check
- **HTTP Method**: `GET`
- **Route**: `/`
- **Purpose**: Verifies that the FastAPI backend server is online and operational.
- **Request Parameters**: None
- **Response Payload**:
  ```json
  {
    "status": "healthy",
    "service": "City Health — Vaccination Outreach Planner API",
    "version": "1.0.0",
    "docs_url": "/docs"
  }
  ```
- **Possible Errors**: None

---

## 🏙️ Area Management Endpoints

### 2. List All City Zones
- **HTTP Method**: `GET`
- **Route**: `/api/areas`
- **Purpose**: Returns aggregate public health indicators across all 12 city zones.
- **Request Parameters**: None
- **Response Payload**: Array of `AreaDetail` objects:
  ```json
  [
    {
      "area_id": "AREA-01",
      "area_name": "Metro Central Corridor",
      "zone_type": "High-Density Urban",
      "population": 18500,
      "eligible_population": 4200,
      "accessibility_index": 0.95,
      "latitude": 40.7128,
      "longitude": -74.0060,
      "distance_from_base_km": 3.2,
      "vaccinated_count": 3100,
      "vaccination_coverage": 73.8,
      "service_gap_ratio": 0.262,
      "historical_demand": 410,
      "seasonal_risk": 0.45,
      "emerging_risk": 0.38,
      "mobility_index": 0.85,
      "inflow_index": 0.90,
      "outflow_index": 0.80
    }
  ]
  ```
- **Possible Errors**: `HTTP 500 Internal Server Error` (Database connection failure)

### 3. Get Single Zone Detail
- **HTTP Method**: `GET`
- **Route**: `/api/areas/{area_id}`
- **Purpose**: Fetches aggregate metrics for a specific zone by ID.
- **Request Parameters**: Path parameter `area_id` (string, e.g. `AREA-07`)
- **Response Payload**: Single `AreaDetail` object.
- **Possible Errors**:
  - `HTTP 404 Not Found`: `{"detail": "Area not found"}`

---

## 🎯 Outreach Planner Endpoints

### 4. Generate Outreach Plan
- **HTTP Method**: `POST`
- **Route**: `/api/planner/generate`
- **Purpose**: Generates prioritized outreach recommendations for a target planning period and objective.
- **Request Body**: `PlanRequest` JSON:
  ```json
  {
    "planning_period": "2026-Q4",
    "num_sessions": 5,
    "session_capacity": 300,
    "max_travel_distance_km": 12.0,
    "objective": "RISK_REDUCTION",
    "reach_weight_pop": 0.45,
    "reach_weight_gap": 0.35,
    "reach_weight_access": 0.20,
    "risk_weight_risk": 0.50,
    "risk_weight_gap": 0.25,
    "risk_weight_mobility": 0.15,
    "risk_weight_pop": 0.10
  }
  ```
- **Response Payload**: Array of `RecommendationResponse` objects sorted by rank ascending.
- **Possible Errors**:
  - `HTTP 422 Unprocessable Entity`: Input validation failure (e.g., `num_sessions > 20`).

### 5. Objective Comparison Matrix
- **HTTP Method**: `POST`
- **Route**: `/api/planner/compare`
- **Purpose**: Computes side-by-side priority ranks across Baseline, Maximum Reach, and Emerging Risk Reduction engines.
- **Request Body**: `PlanRequest` JSON
- **Response Payload**: Array of `PlanComparisonResponse` objects detailing rank differences (`rank_difference = baseline_rank - risk_rank`).

---

## ✍️ Governance & Review Endpoints

### 6. Submit Human Review Decision
- **HTTP Method**: `POST`
- **Route**: `/api/reviews/approve`
- **Purpose**: Allows authorized reviewers to Accept, Modify, Reject, or Override recommendations.
- **Request Body**: `ReviewRequest` JSON:
  ```json
  {
    "recommendation_id": "REC-UUID-1234",
    "reviewer_id": "Dr.Vance",
    "reviewer_role": "Clinician Reviewer",
    "decision": "OVERRIDDEN",
    "override_reason": "Authorized secondary transit bus route",
    "modified_capacity": 300
  }
  ```
- **Response Payload**: `ReviewResponse` JSON with review ID and timestamp.
- **Possible Errors**:
  - `HTTP 404 Not Found`: Recommendation not found.
  - `HTTP 400 Bad Request`: Mandatory override justification reason missing or under 5 characters.

### 7. Retrieve Audit Trail Log
- **HTTP Method**: `GET`
- **Route**: `/api/reviews/audit-trail`
- **Purpose**: Fetches immutable audit trail log of all human reviewer decisions, ordered by timestamp descending.
- **Request Parameters**: None
- **Response Payload**: Array of `ReviewResponse` objects.

### 8. List Recommendations
- **HTTP Method**: `GET`
- **Route**: `/api/reviews/recommendations`
- **Purpose**: Lists generated recommendations, optionally filtered by status (`PENDING`, `ACCEPTED`, `MODIFIED`, `REJECTED`, `OVERRIDDEN`).
- **Query Parameters**: `status` (optional string)
- **Response Payload**: Array of `RecommendationResponse` objects.

---

## 📊 Evaluation & Error Analysis Endpoints

### 9. Compute Evaluation Metrics
- **HTTP Method**: `GET`
- **Route**: `/api/eval/metrics`
- **Purpose**: Calculates quantitative KPIs across all three planning objectives for comparative evaluation.
- **Query Parameters**:
  - `num_sessions` (int, default=5)
  - `capacity` (int, default=300)
  - `max_dist` (float, default=12.0)
- **Response Payload**: Array of 3 `EvalMetricsResponse` objects (one for each objective).

### 10. Get Error Analysis Scenarios
- **HTTP Method**: `GET`
- **Route**: `/api/eval/error-analysis`
- **Purpose**: Returns 4 structured real-world algorithmic failure mode walkthroughs (`ERR-01` to `ERR-04`).
- **Request Parameters**: None
- **Response Payload**: Array of 4 scenario objects detailing area ID, description, consequence, and human mitigation.
