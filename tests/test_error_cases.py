from app.planner.baseline import calculate_baseline_scores
from app.planner.risk_engine import calculate_risk_scores
from app.planner.constraints import evaluate_constraints
from app.planner.evaluator import get_error_analysis_scenarios
from app.data.seed_data import SEED_AREAS

def test_failure_scenario_err_01_capacity_bottleneck():
    """
    ERR-01: Area 07 (Eastside Railway Market) has a severe risk spike (0.96),
    but 3,820 unvaccinated eligible individuals. Single session capacity (300)
    creates a major capacity bottleneck.
    """
    area_07 = next(a for a in SEED_AREAS if a["area_id"] == "AREA-07")
    hard_passed, flags, expected_reach = evaluate_constraints(area_07, session_capacity=300, max_travel_distance_km=12.0)
    
    unvaccinated = area_07["eligible_population"] - area_07["vaccinated_count"]
    assert unvaccinated == 3820
    assert expected_reach == 300  # Capped at session capacity
    assert expected_reach < unvaccinated  # Bottleneck confirmed

def test_failure_scenario_err_02_access_barriers():
    """
    ERR-02: Area 04 (Southside informal Settlement) has accessibility_index = 0.42 (< 0.50),
    triggering SOFT_LOW_ACCESSIBILITY warning for mobile clinic access.
    """
    area_04 = next(a for a in SEED_AREAS if a["area_id"] == "AREA-04")
    hard_passed, flags, expected_reach = evaluate_constraints(area_04, session_capacity=300, max_travel_distance_km=12.0)
    
    assert hard_passed is True
    assert any(f["code"] == "SOFT_LOW_ACCESSIBILITY" for f in flags)

def test_failure_scenario_err_03_historical_lag():
    """
    ERR-03: Area 11 (College Heights Campus) has high mobility (0.96), causing historical baseline
    to rank it lower while Emerging Risk Engine elevates it.
    """
    baseline_scores = {x["area_id"]: x["rank"] for x in calculate_baseline_scores(SEED_AREAS)}
    risk_scores = {x["area_id"]: x["rank"] for x in calculate_risk_scores(SEED_AREAS)}
    
    area_07_baseline_rank = baseline_scores["AREA-07"]
    area_07_risk_rank = risk_scores["AREA-07"]
    
    # AREA-07 ranks #10 in baseline due to historical lag, but #1 in Risk Engine!
    assert area_07_baseline_rank > area_07_risk_rank
    assert area_07_risk_rank == 1

def test_failure_scenario_err_04_resource_competition():
    """
    ERR-04: AREA-04 (0.89 risk) and AREA-07 (0.96 risk) compete for top priority slots.
    """
    scenarios = get_error_analysis_scenarios()
    err_04 = next(s for s in scenarios if s["id"] == "ERR-04")
    assert "AREA-04" in err_04["area_id"]
    assert "AREA-07" in err_04["area_id"]

def test_empty_areas_input_scoring():
    """
    Edge Case: Passing empty list to scoring engines returns empty result cleanly without crash.
    """
    assert calculate_baseline_scores([]) == []
    assert calculate_risk_scores([]) == []
