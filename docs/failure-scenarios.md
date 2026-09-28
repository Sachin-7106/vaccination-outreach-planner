# Failure & Error Analysis Scenarios

This document details 4 real-world algorithmic edge cases and failure modes where automated statistical models struggle or produce suboptimal allocations, demonstrating the necessity of human-in-the-loop clinical review.

---

## 📋 Failure Scenario Summary Matrix

| Scenario ID | Problem | Expected System Behavior | Test Module | Test Status |
|---|---|---|---|---|
| **ERR-01** | Severe emerging risk spike (0.96) in `AREA-07` but 3,820 unvaccinated residents vs 300 session capacity. | Caps `expected_reach` at 300, logs capacity bottleneck warning, prompts Clinician to authorize recurring sessions. | `tests/test_error_cases.py::test_failure_scenario_err_01_capacity_bottleneck` | **PASSED** |
| **ERR-02** | High population density (5,100 eligible) in `AREA-04` with low road access index (0.42). | Flags `SOFT_LOW_ACCESSIBILITY` warning, recommends micro-van transit shuttles or pop-up walk-in points. | `tests/test_error_cases.py::test_failure_scenario_err_02_access_barriers` | **PASSED** |
| **ERR-03** | High student transit mobility (0.98) in `AREA-11` causing historical baseline lag (ranks #10 baseline vs #1 risk). | Emerging Risk Engine integrates transit mobility index to override historical lag and capture transient demand. | `tests/test_error_cases.py::test_failure_scenario_err_03_historical_lag` | **PASSED** |
| **ERR-04** | Resource competition between equivalent high-risk zones (`AREA-04` risk 0.89 vs `AREA-07` risk 0.96). | Mathematical engine ranks `AREA-07` #1 by thin margin; Review console flags tie-breaker for human coordinator override. | `tests/test_error_cases.py::test_failure_scenario_err_04_resource_competition` | **PASSED** |

---

## 🔬 Detailed Scenario Walkthroughs

### Scenario ERR-01: Emerging Risk Spike vs Insufficient Session Supply
- **Target Area**: `AREA-07` (Eastside Railway Market)
- **Problem**: `AREA-07` exhibits a critical emerging disease risk spike (`0.96`), with 3,820 unvaccinated eligible individuals. However, standard single session supply capacity is 300 doses.
- **Automated Engine Result**: Single session reaches less than 8% of vulnerable residents.
- **Clinical Mitigation**: System flags capacity bottleneck and prompts Public Health Director to authorize multi-session pop-up deployments.

### Scenario ERR-02: High Population Density vs Severe Access Barriers
- **Target Area**: `AREA-04` (Southside informal Settlement)
- **Problem**: Large target population (5,100 eligible), but road accessibility index is low (`0.42`) due to narrow unpaved alleys.
- **Automated Engine Result**: Large mobile clinic bus cannot physically park near residents.
- **Clinical Mitigation**: System attaches `SOFT_LOW_ACCESSIBILITY` advisory suggesting micro-van shuttles.

### Scenario ERR-03: Population Mobility Causing Historical Baseline Lag
- **Target Area**: `AREA-11` (College Heights Campus)
- **Problem**: Historical average baseline ranks `AREA-11` low (#10) due to low past resident attendance. However, student inflow mobility index is `0.98`.
- **Automated Engine Result**: Legacy historical planning underallocates resources during peak mobility weeks.
- **Clinical Mitigation**: Emerging Risk Engine incorporates mobility index to elevate `AREA-11` to priority Rank #1.

### Scenario ERR-04: Resource Competition Between Equivalent High-Risk Zones
- **Target Area**: `AREA-04` (Southside Settlement) vs `AREA-07` (Eastside Market)
- **Problem**: Both zones face severe risk (`0.89` vs `0.96`) and compete for the final available mobile clinic unit.
- **Automated Engine Result**: Pure score ranking selects `AREA-07` by a thin mathematical margin, leaving `AREA-04` unserved.
- **Clinical Mitigation**: Review console flags tie-breaker scenarios and provides Outreach Coordinator manual override controls.
