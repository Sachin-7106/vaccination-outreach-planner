# Patient & Person Journeys (Phase 1)

This document describes two complete operational person journeys representing how different urgency levels flow through the Vaccination Outreach Planner without compromising patient privacy or individual medical profiling.

---

## Journey A — Lower Urgency (Routine Community Outreach)

**Context:** Northwood Hills Suburb (`AREA-02`), a suburban community with stable disease risk (0.20), high vaccination coverage (86%), and good geographic access (0.88).

### Workflow Sequence:
1. **Surveillance Monitoring**: Area 02 appears on the Executive Dashboard with green baseline indicators.
2. **Planner Scoring**: The Maximum Eligible Reach Engine calculates a priority score of `0.420`, ranking Area 02 as **#6** in the session queue.
3. **Constraint Validation**: All hard travel distance (6.5 km < 12.0 km) and capacity constraints pass cleanly.
4. **Human Review**: The Outreach Coordinator inspects the recommendation and clicks **Accept**. The session status updates to `ACCEPTED`.
5. **Field Logistics**: Mobile health van deploys to Northwood Community Center on scheduled date.
6. **Metrics Tracking**: Session completes reaching 290 eligible individuals; session utilization recorded at 96.7%.

---

## Journey B — Higher Urgency (Critical Outbreak Response)

**Context:** Eastside Railway Market (`AREA-07`), an under-served mobile vendor settlement experiencing a severe emerging infectious disease risk spike (0.96), low past vaccination coverage (20.4%), low historical session attendance (95 visits), high mobility corridor index (0.91), and moderate accessibility (0.55).

### Workflow Sequence:
1. **Surveillance Risk Alert**: Disease surveillance signal detects a sharp rise in seasonal disease velocity (`emerging_risk = 0.96`).
2. **Historical Baseline Failure**: The Historical Average Baseline ranks Area 07 **#10 out of 12** because past attendance was low (95 visits), missing the outbreak entirely.
3. **Emerging Risk Reduction Engine Elevates Priority**: The Risk Engine combines risk (0.96), service gap (0.796), and mobility (0.91), elevating Area 07 to **Rank #1 Priority**.
4. **Explainability & Constraint Inspection**: The system flags soft constraints (`SOFT_LOW_ACCESSIBILITY`, `SOFT_HIGH_MOBILITY_CORRIDOR`). Recommends positioning mobile pop-up tents directly at the transit hub.
5. **Authorised Clinician Override**: The Clinician Reviewer reviews the explainability breakdown factor bars. Approves the high-priority session and logs: *"Authorized Saturday transit market pop-up deployment"*.
6. **High-Impact Execution**: Mobile outreach team deploys Saturday morning, reaching 300 vulnerable individuals and containing local transmission velocity.
