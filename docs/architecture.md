# System Architecture & Technical Design (Phase 1)

---

## 1. System Topology Diagram

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       React 18 + Vite Web Application                       │
│ ┌───────────────────┐ ┌───────────────────┐ ┌─────────────────────────────┐ │
│ │ Executive Dashboard│ │ Area Explorer Map │ │ Outreach Planner Workspace  │ │
│ └───────────────────┘ └───────────────────┘ └─────────────────────────────┘ │
│ ┌───────────────────┐ ┌───────────────────┐ ┌─────────────────────────────┐ │
│ │ Review Console    │ │ Evaluation Charts │ │ User Journey Walkthroughs   │ │
│ └───────────────────┘ └───────────────────┘ └─────────────────────────────┘ │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ REST API (JSON)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FastAPI Backend Server                           │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ API Routers (/api/areas, /api/planner, /api/reviews, /api/eval)         │ │
│ └────────────────────────────────────┬────────────────────────────────────┘ │
│                                      │                                      │
│ ┌────────────────────────────────────▼────────────────────────────────────┐ │
│ │                      Planning & Scoring Core Engine                     │ │
│ │ - Baseline Engine (Historical Average)                                  │ │
│ │ - Reach Objective Engine (Population, Gap, Accessibility)              │ │
│ │ - Emerging Risk Engine (Risk Velocity, Mobility, Gap, Population)       │ │
│ └────────────────────────────────────┬────────────────────────────────────┘ │
│                                      │                                      │
│ ┌────────────────────────────────────▼────────────────────────────────────┐ │
│ │                    Hard & Soft Constraint Validator Engine              │ │
│ │ - Travel Distance Validator (Hard Limit vs Human Override)              │ │
│ │ - Capacity Allocation Cap Validator (Planned Reach <= Unvaccinated Pool)│ │
│ └────────────────────────────────────┬────────────────────────────────────┘ │
│                                      │                                      │
│ ┌────────────────────────────────────▼────────────────────────────────────┐ │
│ │                    Human Review & Immutable Audit Layer                 │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ SQLAlchemy ORM
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             SQLite Relational Database                      │
│ (areas, service_history, disease_risk, mobility_patterns,                   │
│  outreach_sessions, recommendations, reviews)                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Flow Sequence

1. **User Action**: Public Health Planner configures sessions, capacity, travel limit, and selects objective (e.g. `RISK_REDUCTION`).
2. **API Trigger**: Frontend issues `POST /api/planner/generate`.
3. **Data Fetching**: FastAPI loads aggregate city area statistics from SQLite.
4. **Scoring Execution**:
   - Scores normalized across all areas using min-max scaling.
   - Weighted score calculated according to objective parameters.
5. **Constraint Validation**:
   - Checks if distance exceeds max travel limit.
   - Caps expected reach to unvaccinated eligible pool.
6. **Explainability Generation**: Constructs factor breakdown bars and reason summary.
7. **Human Oversight**: Clinician reviews generated cards in Review Console. Accepts, modifies, or overrides hard constraints with mandatory audit reason.
8. **Audit Persistence**: Decision saved to `reviews` audit log table.
