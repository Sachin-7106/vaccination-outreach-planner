from app.planner.constraints import evaluate_constraints

def test_travel_distance_hard_constraint():
    area = {
        "eligible_population": 2000,
        "vaccinated_count": 500,
        "accessibility_index": 0.8,
        "distance_from_base_km": 15.5  # Exceeds max travel of 12.0
    }
    hard_passed, flags, reach = evaluate_constraints(area, session_capacity=300, max_travel_distance_km=12.0)
    assert hard_passed is False
    assert any(f["code"] == "HARD_TRAVEL_EXCEEDED" for f in flags)
    assert reach == 300

def test_capacity_cap_constraint():
    area = {
        "eligible_population": 500,
        "vaccinated_count": 400,  # Only 100 unvaccinated remaining
        "accessibility_index": 0.8,
        "distance_from_base_km": 5.0
    }
    hard_passed, flags, reach = evaluate_constraints(area, session_capacity=300, max_travel_distance_km=12.0)
    assert hard_passed is True
    # Planned reach scaled down to remaining unvaccinated (100)
    assert reach == 100
    assert any(f["code"] == "SOFT_LIMITED_UNVACCINATED_POOL" for f in flags)
