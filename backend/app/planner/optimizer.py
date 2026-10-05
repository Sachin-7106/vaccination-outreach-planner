import time
import pulp
from typing import List, Dict, Any, Tuple

def solve_outreach_allocation(
    areas_data: List[Dict[str, Any]],
    scored_items: List[Dict[str, Any]],
    num_sessions: int,
    session_capacity: int,
    max_travel_distance_km: float,
    objective_type: str = "RISK_REDUCTION",
    reach_weight_pop: float = 0.45,
    reach_weight_gap: float = 0.35,
    reach_weight_access: float = 0.20,
    risk_weight_risk: float = 0.50,
    risk_weight_gap: float = 0.25,
    risk_weight_mobility: float = 0.15,
    risk_weight_pop: float = 0.10,
    allow_distance_overrides: bool = False,
    allow_duplicate_allocations: bool = False
) -> Dict[str, Any]:
    """
    Formal Integer Linear Programming (ILP) Optimization Engine for Vaccination Outreach Planning.

    Mathematical Formulation:
      Decision Variables:
        x_i in Z+ : Number of outreach sessions allocated to candidate area i
        y_i >= 0  : Expected eligible population reached in area i

      Objective Function:
        Maximize Z = SUM_i [ alpha * y_i + beta * (y_i * risk_i) + gamma * (y_i * gap_i) + delta * (y_i * access_i) + eta * S_i * x_i ]

        where:
          - S_i is the pre-computed engine score (0.0 to 1.0)
          - alpha, beta, gamma, delta are objective-specific weights
          - eta is a tie-breaker weight ensuring high-ranking zones are favored under equivalent reach

      Constraints:
        1. Supply Cap: SUM_i x_i <= num_sessions
        2. Session Reach Cap: y_i <= x_i * session_capacity  for all i
        3. Unvaccinated Population Cap: y_i <= unvaccinated_i  for all i
        4. Travel Distance Constraint: x_i == 0 if distance_i > max_travel_distance_km (unless allow_distance_overrides)
        5. Non-negativity & Integrality: x_i in {0, 1, 2, ...}, y_i >= 0

    Returns structured optimization details including allocations, metadata, and factor contributions.
    """
    start_time = time.time()

    score_lookup = {item["area_id"]: item["priority_score"] for item in scored_items}
    rank_lookup = {item["area_id"]: item["rank"] for item in scored_items}

    # Determine objective coefficients based on requested planning goal
    if objective_type == "MAX_REACH":
        alpha = reach_weight_pop
        beta = 0.10
        gamma = reach_weight_gap
        delta = reach_weight_access
    elif objective_type == "HISTORICAL_BASELINE":
        alpha = 0.30
        beta = 0.10
        gamma = 0.20
        delta = 0.40
    else:  # RISK_REDUCTION (default)
        alpha = risk_weight_pop
        beta = risk_weight_risk * 2.0
        gamma = risk_weight_gap
        delta = risk_weight_mobility

    prob = pulp.LpProblem("Vaccination_Outreach_Optimizer", pulp.LpMaximize)

    x = {}
    y = {}
    area_map = {}

    for area in areas_data:
        aid = area["area_id"]
        area_map[aid] = area
        upper_bound = num_sessions if allow_duplicate_allocations else 1
        x[aid] = pulp.LpVariable(f"x_{aid}", lowBound=0, upBound=upper_bound, cat=pulp.LpInteger)
        y[aid] = pulp.LpVariable(f"y_{aid}", lowBound=0, cat=pulp.LpContinuous)

    # 1. Supply Cap
    prob += (pulp.lpSum([x[aid] for aid in x]) <= num_sessions, "Total_Sessions_Supply_Cap")

    # Objective terms
    obj_terms = []

    for area in areas_data:
        aid = area["area_id"]
        elig = area.get("eligible_population", 0)
        vacc = area.get("vaccinated_count", 0)
        unvacc = max(0, elig - vacc)
        coverage_gap = (1.0 - (vacc / elig)) if elig > 0 else 0.0
        risk = area.get("emerging_risk", 0.0)
        access = area.get("accessibility_index", 0.5)
        dist = area.get("distance_from_base_km", 0.0)
        hist_demand = area.get("historical_demand", 0)
        priority_score = score_lookup.get(aid, 0.0)

        # 2. Reach per session cap
        prob += (y[aid] <= x[aid] * session_capacity, f"Session_Capacity_Cap_{aid}")

        # 3. Unvaccinated demand cap
        prob += (y[aid] <= unvacc, f"Unvaccinated_Demand_Cap_{aid}")

        # 4. Travel Distance Constraint
        if dist > max_travel_distance_km and not allow_distance_overrides:
            prob += (x[aid] == 0, f"Hard_Travel_Constraint_{aid}")

        # Multi-objective terms for this area
        reach_term = alpha * y[aid]
        risk_term = beta * y[aid] * risk
        gap_term = gamma * y[aid] * coverage_gap
        access_term = delta * y[aid] * access
        score_tie_breaker = 0.01 * priority_score * x[aid]

        if objective_type == "HISTORICAL_BASELINE":
            hist_term = 0.5 * y[aid] * (hist_demand / 500.0)
            obj_terms.append(reach_term + risk_term + gap_term + hist_term + score_tie_breaker)
        else:
            obj_terms.append(reach_term + risk_term + gap_term + access_term + score_tie_breaker)

    prob += pulp.lpSum(obj_terms)

    # Solve using CBC solver
    solver = pulp.PULP_CBC_CMD(msg=False)
    status_code = prob.solve(solver)
    status_str = pulp.LpStatus[status_code]

    elapsed_ms = (time.time() - start_time) * 1000.0

    allocations = []
    total_allocated_sessions = 0
    total_expected_reach = 0
    total_risk_weighted_reach = 0.0
    total_coverage_gap_reach = 0.0
    total_access_benefit = 0.0

    if status_str in ["Optimal", "Feasible"]:
        for area in areas_data:
            aid = area["area_id"]
            sess_val = int(round(pulp.value(x[aid]) or 0))
            reach_val = int(round(pulp.value(y[aid]) or 0))

            if sess_val > 0:
                total_allocated_sessions += sess_val
                total_expected_reach += reach_val

                risk = area.get("emerging_risk", 0.0)
                elig = area.get("eligible_population", 0)
                vacc = area.get("vaccinated_count", 0)
                gap = (1.0 - (vacc / elig)) if elig > 0 else 0.0
                access = area.get("accessibility_index", 0.5)

                total_risk_weighted_reach += reach_val * risk
                total_coverage_gap_reach += reach_val * gap
                total_access_benefit += reach_val * access

                allocations.append({
                    "area_id": aid,
                    "area_name": area["area_name"],
                    "zone_type": area["zone_type"],
                    "allocated_sessions": sess_val,
                    "expected_reach": reach_val,
                    "priority_score": score_lookup.get(aid, 0.0),
                    "rank": rank_lookup.get(aid, 99),
                    "distance_from_base_km": area["distance_from_base_km"],
                    "emerging_risk": risk,
                    "accessibility_index": access,
                    "eligible_population": elig,
                    "vaccinated_count": vacc,
                    "unvaccinated_count": max(0, elig - vacc)
                })

        # Sort allocations by priority score / rank
        allocations.sort(key=lambda item: item["rank"])

    obj_val = pulp.value(prob.objective) or 0.0

    explanation = (
        f"Formal ILP Optimization ({status_str}) allocated {total_allocated_sessions} session(s) "
        f"across {len(allocations)} area(s) for expected reach of {total_expected_reach:,} individuals "
        f"under objective {objective_type}."
    )

    return {
        "status": status_str.upper(),
        "is_optimal": status_str == "Optimal",
        "allocated_sessions_count": total_allocated_sessions,
        "total_expected_reach": total_expected_reach,
        "objective_value": round(obj_val, 4),
        "selected_allocations": allocations,
        "factor_contributions": {
            "reach_contribution": total_expected_reach,
            "risk_weighted_reach": round(total_risk_weighted_reach, 2),
            "coverage_gap_reach": round(total_coverage_gap_reach, 2),
            "accessibility_benefit": round(total_access_benefit, 2)
        },
        "optimization_metadata": {
            "solver": "PuLP CBC (Integer Linear Programming)",
            "execution_time_ms": round(elapsed_ms, 2),
            "num_variables": len(prob.variables()),
            "num_constraints": len(prob.constraints),
            "status": status_str,
            "allow_distance_overrides": allow_distance_overrides
        },
        "explanation": explanation
    }
