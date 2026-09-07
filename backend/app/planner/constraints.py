def evaluate_constraints(area_dict, session_capacity, max_travel_distance_km):
    """
    Evaluates hard and soft operational constraints for a given candidate area.
    Returns:
      - hard_constraint_passed (bool)
      - flags (list of dicts with code, severity, message)
      - expected_reach (int)
    """
    flags = []
    hard_passed = True

    distance = area_dict.get("distance_from_base_km", 0.0)
    eligible = area_dict.get("eligible_population", 0)
    vaccinated = area_dict.get("vaccinated_count", 0)
    unvaccinated = max(0, eligible - vaccinated)
    accessibility = area_dict.get("accessibility_index", 1.0)
    mobility = area_dict.get("mobility_index", 0.0)
    hist_demand = area_dict.get("historical_demand", 0)

    # 1. HARD CONSTRAINT: Max Travel Distance
    if distance > max_travel_distance_km:
        hard_passed = False
        flags.append({
            "code": "HARD_TRAVEL_EXCEEDED",
            "severity": "HARD",
            "message": f"Travel distance ({distance:.1f} km) exceeds operational maximum ({max_travel_distance_km:.1f} km). Explicit human override required."
        })

    # 2. HARD CONSTRAINT: Capacity Cap Allocation
    # Planned reach cannot exceed unvaccinated population or session capacity
    expected_reach = min(unvaccinated, session_capacity)
    if unvaccinated < session_capacity:
        flags.append({
            "code": "SOFT_LIMITED_UNVACCINATED_POOL",
            "severity": "SOFT",
            "message": f"Session capacity ({session_capacity}) exceeds remaining unvaccinated population ({unvaccinated}). Capacity will be scaled down to {expected_reach}."
        })

    # 3. SOFT CONSTRAINT: Low Geographic Accessibility
    if accessibility < 0.50:
        flags.append({
            "code": "SOFT_LOW_ACCESSIBILITY",
            "severity": "SOFT",
            "message": f"Area accessibility index is low ({accessibility:.2f}). Mobile unit shuttle or pop-up equipment suggested."
        })

    # 4. SOFT CONSTRAINT: High Mobility Corridor
    if mobility > 0.85:
        flags.append({
            "code": "SOFT_HIGH_MOBILITY_CORRIDOR",
            "severity": "SOFT",
            "message": f"High population mobility index ({mobility:.2f}). Schedule sessions near major transit hubs or markets."
        })

    # 5. SOFT CONSTRAINT: Low Historical Attendance History
    if hist_demand < 120:
        flags.append({
            "code": "SOFT_LOW_HISTORICAL_ATTENDANCE",
            "severity": "SOFT",
            "message": f"Low historical session attendance ({hist_demand}). Community health worker pre-engagement advised."
        })

    return hard_passed, flags, expected_reach
