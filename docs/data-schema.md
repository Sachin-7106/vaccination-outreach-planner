# Data Schema Specification (Phase 1)

This document details the relational database schema implemented in SQLite for Phase 1. All data represents aggregate non-discriminatory city zone metrics.

---

## 1. Table Definitions

### `areas`
Primary entity representing aggregate city geographic zones.
- `area_id` (VARCHAR(20), PRIMARY KEY): Unique zone identifier (e.g. `AREA-01`).
- `area_name` (VARCHAR(100)): Zone name (e.g. `Metro Central Corridor`).
- `zone_type` (VARCHAR(50)): Category (e.g. `High-Density Urban`, `Under-Served Settlement`).
- `population` (INT): Total zone population.
- `eligible_population` (INT): Target unvaccinated/vulnerable population.
- `accessibility_index` (FLOAT): Score from 0.0 (poor road access) to 1.0 (excellent).
- `latitude` (FLOAT), `longitude` (FLOAT): Geographic coordinates.
- `distance_from_base_km` (FLOAT): Distance from central health department base.

### `service_history`
Past outreach attendance history.
- `id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `area_id` (VARCHAR(20), FOREIGN KEY -> `areas.area_id`)
- `time_period` (VARCHAR(20)): Planning period (e.g. `2026-Q4`).
- `eligible_population` (INT)
- `vaccinated_count` (INT): Number of vaccinated residents.
- `service_visits` (INT): Number of past mobile unit visits.
- `historical_demand` (INT): Historical average session attendance.

### `disease_risk`
Surveillance signals for seasonal infectious disease.
- `id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `area_id` (VARCHAR(20), FOREIGN KEY -> `areas.area_id`)
- `time_period` (VARCHAR(20))
- `seasonal_risk` (FLOAT): Baseline seasonal risk (0.0 to 1.0).
- `emerging_risk` (FLOAT): Disease velocity / case spike signal (0.0 to 1.0).
- `surveillance_signal_date` (DATE)

### `mobility_patterns`
Population movement patterns.
- `id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `area_id` (VARCHAR(20), FOREIGN KEY -> `areas.area_id`)
- `time_period` (VARCHAR(20))
- `mobility_index` (FLOAT): Overall movement index (0.0 to 1.0).
- `inflow_index` (FLOAT), `outflow_index` (FLOAT)

### `recommendations`
System-generated recommendations.
- `recommendation_id` (VARCHAR(36), PRIMARY KEY)
- `area_id` (VARCHAR(20), FOREIGN KEY -> `areas.area_id`)
- `planning_period` (VARCHAR(20))
- `objective` (VARCHAR(50)): `MAX_REACH`, `RISK_REDUCTION`, or `HISTORICAL_BASELINE`.
- `priority_score` (FLOAT)
- `rank` (INT)
- `expected_reach` (INT)
- `reason` (TEXT): JSON factor breakdown string.
- `hard_constraint_passed` (BOOLEAN)
- `constraint_flags` (TEXT): JSON array string of warning/hard flags.
- `status` (VARCHAR(30)): `PENDING`, `ACCEPTED`, `MODIFIED`, `REJECTED`, or `OVERRIDDEN`.

### `reviews`
Immutable audit log of human reviewer decisions.
- `review_id` (VARCHAR(36), PRIMARY KEY)
- `recommendation_id` (VARCHAR(36), FOREIGN KEY -> `recommendations.recommendation_id`)
- `reviewer_id` (VARCHAR(50)): Reviewer identifier (e.g. `Clinician.Dr-Vance`).
- `reviewer_role` (VARCHAR(50)): Reviewer role.
- `decision` (VARCHAR(30)): `ACCEPTED`, `MODIFIED`, `REJECTED`, or `OVERRIDDEN`.
- `override_reason` (TEXT): Required justification statement for overrides.
- `modified_capacity` (INT)
- `timestamp` (DATETIME)
