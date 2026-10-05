# Role-Based Access Control (RBAC) & Authentication Specification

## Overview
The Vaccination Outreach Planner enforces backend-authoritative authentication and Role-Based Access Control (RBAC) to ensure clinical decision integrity and administrative oversight. The frontend interface never serves as an authorization boundary; all HTTP endpoints independently inspect signed JSON Web Tokens (JWT) provided in the `Authorization: Bearer <token>` header.

---

## 1. Roles & System Personas

| Role | Persona | Key Responsibilities |
|---|---|---|
| `CLINICIAN` | Clinical Field Officer / Public Health Specialist | Evaluates recommended outreach plans, views factor score breakdowns, submits `ACCEPTED`, `MODIFIED` (capacity/range), and `REJECTED` decisions. Cannot override hard constraints. |
| `ADMIN` | Public Health Director / Chief Epidemiologist | Full administrative authority. Manages system configurations, reviews immutable audit trails, and holds exclusive authority to perform `OVERRIDDEN` actions for hard constraint violations with mandatory justification. |

---

## 2. Permissions Matrix

| Endpoint | Method | Unauthenticated | CLINICIAN | ADMIN |
|---|---|---|---|---|
| `/api/auth/login` | `POST` | Allowed | Allowed | Allowed |
| `/api/auth/me` | `GET` | 401 | Allowed | Allowed |
| `/api/planner/generate` | `POST` | 401 | Allowed | Allowed |
| `/api/planner/compare` | `POST` | 401 | Allowed | Allowed |
| `/api/areas` | `GET` | 401 | Allowed | Allowed |
| `/api/areas/{id}` | `GET` | 401 | Allowed | Allowed |
| `/api/areas/geojson` | `GET` | Allowed / Public | Allowed | Allowed |
| `/api/reviews/recommendations` | `GET` | 401 | Allowed | Allowed |
| `/api/reviews/approve` (ACCEPTED/MODIFIED/REJECTED) | `POST` | 401 | Allowed | Allowed |
| `/api/reviews/approve` (OVERRIDDEN) | `POST` | 401 | **403 Forbidden** | **Allowed** |
| `/api/reviews/audit-trail` | `GET` | 401 | Allowed | Allowed |
| `/api/forecast` | `GET` | 401 | Allowed | Allowed |
| `/health` | `GET` | Allowed | Allowed | Allowed |
| `/readiness` | `GET` | Allowed | Allowed | Allowed |

---

## 3. HTTP Error Response Codes

- **HTTP 401 Unauthorized**: Returned when no token is supplied, an expired token is presented, or token signature validation fails.
- **HTTP 403 Forbidden**: Returned when a valid token is supplied, but the user's role lacks permission for the requested operation (e.g. a Clinician attempting an `OVERRIDDEN` decision).
- **HTTP 409 Conflict**: Returned when an operation violates state transition rules or a concurrent review collision is detected.
- **HTTP 422 Unprocessable Entity**: Returned when request body parameters fail validation bounds (e.g. negative capacity or invalid decision strings).

---

## 4. Hard Constraint Override Policy

Overriding a hard operational constraint (e.g. deploying a mobile clinic beyond the standard vehicle travel radius):
1. **Requires ADMIN Role**: Clinicians attempting an override will receive HTTP 403.
2. **Mandatory Documentation**: The request must include an `override_reason` string of at least 5 non-whitespace characters explaining the operational rationale (e.g., "Special logistics clearance granted for remote outbreak zone").
3. **Audit Trail Logging**: All overrides are permanently recorded in the append-only `reviews` table with timestamp, admin ID, and reason.

---

## 5. Demo Credentials (Development Only)

> [!WARNING]
> These credentials are for local development and integration testing only. In production, real user accounts should be seeded via secure environment scripts with unique strong passwords.

- **Admin Account**:
  - Username: `admin`
  - Password: `AdminPass123!`
  - Role: `ADMIN`

- **Clinician Account**:
  - Username: `clinician`
  - Password: `ClinicianPass123!`
  - Role: `CLINICIAN`
