def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_list_areas_api(client):
    response = client.get("/api/areas")
    assert response.status_code == 200
    areas = response.json()
    assert len(areas) == 12  # 12 seed areas
    first = areas[0]
    assert "area_id" in first
    assert "vaccination_coverage" in first
    assert "service_gap_ratio" in first

def test_get_single_area_api(client):
    response = client.get("/api/areas/AREA-01")
    assert response.status_code == 200
    area = response.json()
    assert area["area_id"] == "AREA-01"
    assert area["area_name"] == "Metro Central Corridor"

def test_get_single_area_not_found(client):
    response = client.get("/api/areas/AREA-NONEXISTENT")
    assert response.status_code == 404
    assert response.json()["detail"] == "Area not found"

def test_planner_generate_api(client):
    payload = {
        "planning_period": "2026-Q4",
        "num_sessions": 3,
        "session_capacity": 300,
        "max_travel_distance_km": 12.0,
        "objective": "RISK_REDUCTION"
    }
    response = client.post("/api/planner/generate", json=payload)
    assert response.status_code == 200
    recs = response.json()
    assert len(recs) == 3
    assert recs[0]["objective"] == "RISK_REDUCTION"
    assert recs[0]["rank"] == 1

def test_planner_generate_baseline_api(client):
    payload = {
        "planning_period": "2026-Q4",
        "num_sessions": 5,
        "session_capacity": 300,
        "max_travel_distance_km": 12.0,
        "objective": "HISTORICAL_BASELINE"
    }
    response = client.post("/api/planner/generate", json=payload)
    assert response.status_code == 200
    recs = response.json()
    assert len(recs) == 5
    assert recs[0]["objective"] == "HISTORICAL_BASELINE"

def test_planner_compare_api(client):
    payload = {
        "planning_period": "2026-Q4",
        "num_sessions": 5,
        "session_capacity": 300,
        "max_travel_distance_km": 12.0,
        "objective": "RISK_REDUCTION"
    }
    response = client.post("/api/planner/compare", json=payload)
    assert response.status_code == 200
    comparison = response.json()
    assert len(comparison) == 12
    first = comparison[0]
    assert "baseline_rank" in first
    assert "risk_rank" in first
    assert "rank_difference" in first

def test_eval_metrics_api(client):
    response = client.get("/api/eval/metrics?num_sessions=5&capacity=300&max_dist=12.0")
    assert response.status_code == 200
    metrics = response.json()
    assert len(metrics) == 3  # HISTORICAL_BASELINE, MAX_REACH, RISK_REDUCTION
    objectives = [m["objective"] for m in metrics]
    assert "HISTORICAL_BASELINE" in objectives
    assert "MAX_REACH" in objectives
    assert "RISK_REDUCTION" in objectives

def test_eval_error_analysis_api(client):
    response = client.get("/api/eval/error-analysis")
    assert response.status_code == 200
    scenarios = response.json()
    assert len(scenarios) == 4
    assert scenarios[0]["id"] == "ERR-01"

def test_invalid_planner_payload_api(client):
    # Session count > 20 should trigger Pydantic validation error (422)
    payload = {
        "num_sessions": 100,
        "session_capacity": 300
    }
    response = client.post("/api/planner/generate", json=payload)
    assert response.status_code == 422
