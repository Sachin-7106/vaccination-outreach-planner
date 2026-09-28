from app.planner.evaluator import compute_evaluation_metrics, get_error_analysis_scenarios

def test_compute_evaluation_metrics_basic():
    recs = [
        {
            "area_id": "AREA-01",
            "expected_reach": 300,
            "hard_constraint_passed": True,
            "reason": {
                "metrics_snapshot": {
                    "unvaccinated_count": 1000,
                    "emerging_risk": 0.50
                }
            }
        },
        {
            "area_id": "AREA-02",
            "expected_reach": 200,
            "hard_constraint_passed": False,
            "reason": {
                "metrics_snapshot": {
                    "unvaccinated_count": 500,
                    "emerging_risk": 0.80
                }
            }
        }
    ]

    metrics = compute_evaluation_metrics(recs, num_sessions=2, session_capacity=300)

    # total_reach = 300 + 200 = 500
    assert metrics["total_eligible_reached"] == 500
    # total_capacity = 2 * 300 = 600
    assert metrics["total_capacity_allocated"] == 600
    # utilisation = 500 / 600 * 100 = 83.33 -> 83.3
    assert metrics["session_utilisation_rate"] == 83.3
    # reached per session = 500 / 2 = 250.0
    assert metrics["eligible_reached_per_session"] == 250.0
    # areas served = 2
    assert metrics["areas_served_count"] == 2
    # feasibility rate = 1 / 2 * 100 = 50.0%
    assert metrics["travel_feasibility_rate"] == 50.0
    # risk sum = 300*0.5 + 200*0.8 = 150 + 160 = 310. risk_weighted = 310 / 500 = 0.62
    assert metrics["risk_weighted_coverage_score"] == 0.62
    # total unvaccinated = 1000 + 500 = 1500; unmet = 1500 - 500 = 1000
    assert metrics["unmet_eligible_demand"] == 1000

def test_compute_evaluation_metrics_empty():
    metrics = compute_evaluation_metrics([], num_sessions=5, session_capacity=300)
    assert metrics["total_eligible_reached"] == 0
    assert metrics["session_utilisation_rate"] == 0.0
    assert metrics["areas_served_count"] == 0
    assert metrics["travel_feasibility_rate"] == 0.0

def test_error_analysis_scenarios_count():
    scenarios = get_error_analysis_scenarios()
    assert len(scenarios) == 4
    scenario_ids = [s["id"] for s in scenarios]
    assert "ERR-01" in scenario_ids
    assert "ERR-02" in scenario_ids
    assert "ERR-03" in scenario_ids
    assert "ERR-04" in scenario_ids
