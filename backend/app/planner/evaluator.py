def compute_evaluation_metrics(recommendations_list, num_sessions, session_capacity):
    """
    Computes empirical performance metrics for a generated outreach plan.

    Why this function exists:
      Allows public health planners to quantitatively compare different planning models
      (Historical Baseline vs Maximum Reach vs Emerging Risk Reduction) on key KPIs:
      - Eligible population reached
      - Supply capacity utilization rate
      - Unmet eligible demand
      - Risk-weighted population coverage
      - Fleet travel feasibility rate

    Formulae:
      - Total Capacity Allocated = num_sessions * session_capacity
      - Session Utilization Rate = (total_reach / total_capacity) * 100
      - Risk-Weighted Coverage = Sum(expected_reach * emerging_risk) / total_reach
      - Travel Feasibility Rate = (hard_constraint_passed_count / num_sessions) * 100
    """
    if not recommendations_list or num_sessions <= 0:
        return {
            "eligible_reached_per_session": 0.0,
            "total_eligible_reached": 0,
            "total_capacity_allocated": 0,
            "session_utilisation_rate": 0.0,
            "unmet_eligible_demand": 0,
            "areas_served_count": 0,
            "risk_weighted_coverage_score": 0.0,
            "travel_feasibility_rate": 0.0
        }

    top_recs = recommendations_list[:num_sessions]

    total_reach = sum(rec["expected_reach"] for rec in top_recs)
    total_capacity = num_sessions * session_capacity
    utilisation = (total_reach / total_capacity * 100) if total_capacity > 0 else 0.0
    reached_per_session = total_reach / num_sessions

    # Count how many selected zones satisfy all operational hard constraints without requiring human override
    feasible_count = sum(1 for rec in top_recs if rec["hard_constraint_passed"])
    feasibility_rate = (feasible_count / len(top_recs) * 100) if top_recs else 100.0

    # Risk-weighted coverage: measures whether allocated doses target high-risk epicenters
    risk_sum = 0.0
    for rec in top_recs:
        snap = rec["reason"]["metrics_snapshot"]
        risk_sum += rec["expected_reach"] * snap["emerging_risk"]
    risk_weighted_score = (risk_sum / total_reach) if total_reach > 0 else 0.0

    # Calculate remaining unserved vulnerable population across target zones
    total_unmet = sum(rec["reason"]["metrics_snapshot"]["unvaccinated_count"] - rec["expected_reach"] for rec in top_recs)

    return {
        "eligible_reached_per_session": round(reached_per_session, 1),
        "total_eligible_reached": total_reach,
        "total_capacity_allocated": total_capacity,
        "session_utilisation_rate": round(utilisation, 1),
        "unmet_eligible_demand": max(0, total_unmet),
        "areas_served_count": len(top_recs),
        "risk_weighted_coverage_score": round(risk_weighted_score, 3),
        "travel_feasibility_rate": round(feasibility_rate, 1)
    }

def get_error_analysis_scenarios():
    """
    Returns 4 structured algorithmic failure mode walkthroughs demonstrating real-world conditions
    where purely automated statistical ranking struggles, justifying the necessity of human review.
    """
    return [
        {
            "id": "ERR-01",
            "title": "Emerging Risk Spike vs Insufficient Session Capacity",
            "area_id": "AREA-07",
            "area_name": "Eastside Railway Market",
            "description": "Area 07 experiences a severe seasonal disease risk spike (0.96), but has 3,820 unvaccinated eligible individuals. A single mobile session capacity (300 doses) reaches less than 8% of the vulnerable population.",
            "consequence": "High remaining disease transmission risk despite successful single session execution.",
            "mitigation": "Planner highlights capacity bottleneck and prompts Clinician Reviewer to authorize recurring pop-up sessions."
        },
        {
            "id": "ERR-02",
            "title": "High Population Density vs Severe Access Barriers",
            "area_id": "AREA-04",
            "area_name": "Southside informal Settlement",
            "description": "Area 04 has 5,100 eligible people, but accessibility index is extremely low (0.42) due to narrow unpaved roads unsuitable for large mobile clinic buses.",
            "consequence": "Mobile clinic vehicle cannot physically park near target population, resulting in unused session capacity.",
            "mitigation": "Flagged with SOFT_LOW_ACCESSIBILITY. Recommends micro-van transit shuttle or community center walk-in points."
        },
        {
            "id": "ERR-03",
            "title": "High Population Mobility Causing Historical Data Misleading Lag",
            "area_id": "AREA-11",
            "area_name": "College Heights Campus",
            "description": "Historical average baseline ranks Area 11 low because past resident attendance was 380. However, transit mobility inflow is 0.98 due to seasonal student population shifts.",
            "consequence": "Historical baseline underallocates resources during peak mobility weeks.",
            "mitigation": "Emerging Risk Objective integrates mobility index to override historical lag and capture transient demand."
        },
        {
            "id": "ERR-04",
            "title": "Resource Competition Between Equivalent High-Risk Zones",
            "area_id": "AREA-04 & AREA-07",
            "area_name": "Southside Settlement & Eastside Market",
            "description": "Both Area 04 (0.89 risk) and Area 07 (0.96 risk) compete for the last available mobile outreach session slot.",
            "consequence": "Mathematical score ranking selects Area 07 by a thin margin (0.96 vs 0.89), leaving Area 04 unserved.",
            "mitigation": "Review console flags tie-breaker scenarios and gives Outreach Coordinator manual override to adjust session distribution."
        }
    ]
