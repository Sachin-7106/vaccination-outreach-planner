# System Requirements Specification (Phase 1)

**Project Title:** Vaccination Outreach Planner for Mobile & Under-Served Populations

---

## 1. Functional Requirements (FR)

- **FR1 — Surveillance Dashboard**: Display aggregate population, eligible target population, historical vaccination coverage, emerging risk score, mobility index, and session capacity utilization.
- **FR2 — Area Comparison Workspace**: Allow staff to compare city areas side-by-side across historical demand vs emerging risk velocity.
- **FR3 — Outreach Planner Configuration**: Allow authorized staff to configure planning period, available sessions, session capacity, max travel distance, and select planning objective.
- **FR4 — Recommendation Engine**: Generate ranked session recommendations for Objective A (Max Reach), Objective B (Emerging Risk Reduction), and Baseline.
- **FR5 — Explainability Factor Breakdown**: Display mathematical score derivation, normalized factor weights, and plain-language reason summary for every recommendation.
- **FR6 — Human Review & Override**: Staff can Accept, Modify, Reject, or Override recommendations. Overrides require mandatory justification logging.
- **FR7 — Comparative Metrics & Evaluation**: Calculate primary metric (*Eligible people reached per session*), utilization rate, risk-weighted coverage, and display 4 error analysis failure modes.

---

## 2. Non-Functional Requirements (NFR)

- **NFR1 — Privacy & Data Minimisation**: System uses aggregate area-level statistics only. No Personally Identifiable Information (PII) or individual medical records are stored.
- **NFR2 — Responsible AI & Non-Discrimination**: Prioritization uses aggregate risk, service gap, accessibility, and capacity. No protected traits (race, religion, gender, ethnicity) are processed.
- **NFR3 — Human-in-the-Loop Oversight**: Algorithmic outputs are strict recommendations. Final approval requires explicit human action by an authorized reviewer.
- **NFR4 — Explainability & Transparency**: 100% of recommendation scores are mathematically interpretable and visually broken down into normalized factors.
- **NFR5 — Auditability**: All human decisions (accept/modify/reject/override) are permanently logged with reviewer ID, timestamp, and justification reason.
- **NFR6 — Security & Access Control**: Simulated Role-Based Access Control (RBAC) separates Planner, Outreach Coordinator, and Clinician Reviewer permissions.
- **NFR7 — Performance**: Recommendation scoring generation across 12 city zones executes in <200 ms.
- **NFR8 — Usability & Accessibility**: Responsive, high-contrast healthcare dashboard theme meeting WCAG 2.1 AA standards.
