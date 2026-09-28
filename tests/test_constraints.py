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

def test_soft_low_accessibility_constraint():
    area = {
        "eligible_population": 3000,
        "vaccinated_count": 1000,
        "accessibility_index": 0.42,  # < 0.50
        "distance_from_base_km": 4.0
    }
    hard_passed, flags, reach = evaluate_constraints(area, session_capacity=300, max_travel_distance_km=12.0)
    assert hard_passed is True
    assert any(f["code"] == "SOFT_LOW_ACCESSIBILITY" for f in flags)

def test_soft_high_mobility_corridor_constraint():
    area = {
        "eligible_population": 4000,
        "vaccinated_count": 2000,
        "accessibility_index": 0.90,
        "mobility_index": 0.94,  # > 0.85
        "distance_from_base_km": 5.0
    }
    hard_passed, flags, reach = evaluate_constraints(area, session_capacity=300, max_travel_distance_km=12.0)
    assert hard_passed is True
    assert any(f["code"] == "SOFT_HIGH_MOBILITY_CORRIDOR" for f in flags)

def test_soft_low_historical_attendance_constraint():
    area = {
        "eligible_population": 4000,
        "vaccinated_count": 1000,
        "historical_demand": 95,  # < 120
        "distance_from_base_km": 5.0
    }
    hard_passed, flags, reach = evaluate_constraints(area, session_capacity=300, max_travel_distance_km=12.0)
    assert hard_passed is True
    assert any(f["code"] == "SOFT_LOW_HISTORICAL_ATTENDANCE" for f in flags)

def test_zero_unvaccinated_pool():
    area = {
        "eligible_population": 1000,
        "vaccinated_count": 1000,  # 100% vaccinated
        "distance_from_base_km": 5.0
    }
    hard_passed, flags, reach = evaluate_constraints(area, session_capacity=300, max_travel_distance_km=12.0)
    assert hard_passed is True
    assert reach == 0
