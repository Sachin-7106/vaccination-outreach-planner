import pytest
import threading
from app.models.schema import Recommendation, Review, User
from app.planner.optimizer import solve_outreach_allocation
from app.core.database import SessionLocal

def test_1_authenticated_plan_generation(client, clinician_headers):
    payload = {
        "planning_period": "2026-Q4",
        "num_sessions": 4,
        "session_capacity": 300,
        "max_travel_distance_km": 12.0,
        "objective": "RISK_REDUCTION"
    }
    res = client.post("/api/planner/generate", json=payload, headers=clinician_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 4
    for rec in data:
        assert rec["status"] == "PENDING"
        assert "optimization_metadata" in rec["reason"]

def test_2_successful_clinician_review(client, db_session, clinician_headers):
    rec = Recommendation(
        recommendation_id="REC-CLIN-01",
        area_id="AREA-01",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.92,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=True,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    res = client.post("/api/reviews/approve", json={
        "recommendation_id": "REC-CLIN-01",
        "decision": "ACCEPTED"
    }, headers=clinician_headers)
    assert res.status_code == 200
    assert res.json()["decision"] == "ACCEPTED"
    assert res.json()["reviewer_role"] == "CLINICIAN"

def test_3_admin_override(client, db_session, admin_headers):
    rec = Recommendation(
        recommendation_id="REC-ADM-OVERRIDE",
        area_id="AREA-09",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.88,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=False,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    res = client.post("/api/reviews/approve", json={
        "recommendation_id": "REC-ADM-OVERRIDE",
        "decision": "OVERRIDDEN",
        "override_reason": "Logistics shuttle van pre-allocated for long distance zone"
    }, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["decision"] == "OVERRIDDEN"
    assert res.json()["reviewer_role"] == "ADMIN"

def test_4_unauthenticated_review_attempt(client):
    res = client.post("/api/reviews/approve", json={
        "recommendation_id": "REC-CLIN-01",
        "decision": "ACCEPTED"
    })
    assert res.status_code == 401

def test_5_clinician_attempting_admin_override(client, db_session, clinician_headers):
    rec = Recommendation(
        recommendation_id="REC-CLIN-FAIL-OVERRIDE",
        area_id="AREA-09",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.88,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=False,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    res = client.post("/api/reviews/approve", json={
        "recommendation_id": "REC-CLIN-FAIL-OVERRIDE",
        "decision": "OVERRIDDEN",
        "override_reason": "Clinician trying to override"
    }, headers=clinician_headers)
    assert res.status_code == 403
    assert "Clinicians are not authorized" in res.json()["detail"]

def test_6_invalid_recommendation_id(client, clinician_headers):
    res = client.post("/api/reviews/approve", json={
        "recommendation_id": "NON-EXISTENT-REC-ID",
        "decision": "ACCEPTED"
    }, headers=clinician_headers)
    assert res.status_code == 404

def test_7_invalid_state_transition_duplicate_review(client, db_session, clinician_headers):
    rec = Recommendation(
        recommendation_id="REC-STATE-01",
        area_id="AREA-01",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.90,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=True,
        status="ACCEPTED"
    )
    db_session.add(rec)
    db_session.commit()

    res = client.post("/api/reviews/approve", json={
        "recommendation_id": "REC-STATE-01",
        "decision": "ACCEPTED"
    }, headers=clinician_headers)
    assert res.status_code == 409
    assert "already been finalized" in res.json()["detail"]

def test_8_hard_constraint_violation(client, clinician_headers):
    # AREA-09 distance is 16.5km > 12.0km max travel distance
    payload = {
        "planning_period": "2026-Q4",
        "num_sessions": 10,
        "session_capacity": 300,
        "max_travel_distance_km": 5.0,
        "objective": "RISK_REDUCTION"
    }
    res = client.post("/api/planner/generate", json=payload, headers=clinician_headers)
    assert res.status_code == 200
    for rec in res.json():
        assert rec["distance_from_base_km"] <= 5.0

def test_9_hard_constraint_override_without_reason(client, db_session, admin_headers):
    rec = Recommendation(
        recommendation_id="REC-NO-REASON",
        area_id="AREA-09",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.88,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=False,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    res = client.post("/api/reviews/approve", json={
        "recommendation_id": "REC-NO-REASON",
        "decision": "OVERRIDDEN",
        "override_reason": ""
    }, headers=admin_headers)
    assert res.status_code in [400, 422]

def test_10_invalid_modified_capacity(client, db_session, clinician_headers):
    rec = Recommendation(
        recommendation_id="REC-BAD-CAP",
        area_id="AREA-01",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.90,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=True,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    res = client.post("/api/reviews/approve", json={
        "recommendation_id": "REC-BAD-CAP",
        "decision": "MODIFIED",
        "modified_capacity": -50
    }, headers=clinician_headers)
    assert res.status_code == 422

def test_11_concurrent_review_requests(client, db_session, clinician_headers):
    rec = Recommendation(
        recommendation_id="REC-CONCURRENT-01",
        area_id="AREA-01",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.90,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=True,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    results = []

    def submit_a():
        r = client.post("/api/reviews/approve", json={
            "recommendation_id": "REC-CONCURRENT-01",
            "decision": "ACCEPTED"
        }, headers=clinician_headers)
        results.append(r.status_code)

    def submit_b():
        r = client.post("/api/reviews/approve", json={
            "recommendation_id": "REC-CONCURRENT-01",
            "decision": "REJECTED"
        }, headers=clinician_headers)
        results.append(r.status_code)

    t1 = threading.Thread(target=submit_a)
    t2 = threading.Thread(target=submit_b)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Exactly one request succeeds (200), and the other fails with conflict (409)
    assert 200 in results
    assert 409 in results

def test_12_audit_record_persistence(client, db_session, clinician_headers):
    rec = Recommendation(
        recommendation_id="REC-PERSIST-01",
        area_id="AREA-02",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.85,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=True,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    client.post("/api/reviews/approve", json={
        "recommendation_id": "REC-PERSIST-01",
        "decision": "ACCEPTED"
    }, headers=clinician_headers)

    res = client.get("/api/reviews/audit-trail", headers=clinician_headers)
    assert res.status_code == 200
    logs = res.json()
    assert any(log["recommendation_id"] == "REC-PERSIST-01" for log in logs)

def test_13_optimization_constraints():
    areas = [
        {"area_id": "A1", "area_name": "Zone 1", "zone_type": "Urban", "eligible_population": 1000, "vaccinated_count": 200, "distance_from_base_km": 5.0, "emerging_risk": 0.8, "accessibility_index": 0.9},
        {"area_id": "A2", "area_name": "Zone 2", "zone_type": "Suburb", "eligible_population": 500, "vaccinated_count": 100, "distance_from_base_km": 15.0, "emerging_risk": 0.9, "accessibility_index": 0.8}
    ]
    scored = [
        {"area_id": "A1", "priority_score": 0.85, "rank": 1},
        {"area_id": "A2", "priority_score": 0.95, "rank": 2}
    ]

    res = solve_outreach_allocation(
        areas_data=areas,
        scored_items=scored,
        num_sessions=2,
        session_capacity=300,
        max_travel_distance_km=10.0,
        objective_type="RISK_REDUCTION"
    )
    assert res["status"] in ["OPTIMAL", "FEASIBLE"]
    assert res["allocated_sessions_count"] <= 2
    # Zone A2 exceeds 10km travel limit, so it must get 0 sessions
    for alloc in res["selected_allocations"]:
        assert alloc["area_id"] != "A2"
        assert alloc["allocated_sessions"] >= 0

def test_14_optimization_infeasible_case():
    areas = [
        {"area_id": "A1", "area_name": "Far Zone", "zone_type": "Rural", "eligible_population": 1000, "vaccinated_count": 200, "distance_from_base_km": 25.0, "emerging_risk": 0.8, "accessibility_index": 0.5}
    ]
    scored = [{"area_id": "A1", "priority_score": 0.85, "rank": 1}]

    res = solve_outreach_allocation(
        areas_data=areas,
        scored_items=scored,
        num_sessions=1,
        session_capacity=300,
        max_travel_distance_km=10.0,
        objective_type="RISK_REDUCTION"
    )
    # Since distance > max_dist, zero sessions allocated
    assert res["allocated_sessions_count"] == 0

def test_15_objective_comparison_matrix(client, clinician_headers):
    res = client.post("/api/planner/compare", json={
        "planning_period": "2026-Q4",
        "num_sessions": 5,
        "session_capacity": 300,
        "max_travel_distance_km": 12.0,
        "objective": "RISK_REDUCTION"
    }, headers=clinician_headers)
    assert res.status_code == 200
    comp = res.json()
    assert len(comp) == 12

def test_16_eval_metrics_endpoint(client, clinician_headers):
    res = client.get("/api/eval/metrics?num_sessions=5&capacity=300&max_dist=12.0", headers=clinician_headers)
    assert res.status_code == 200
    metrics = res.json()
    assert len(metrics) == 3

def test_17_forecast_endpoint(client, clinician_headers):
    res = client.get("/api/forecast", headers=clinician_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 12
    assert "forecasts" in data[0]

def test_18_gis_geojson_endpoint(client):
    res = client.get("/api/areas/geojson")
    assert res.status_code == 200
    geojson = res.json()
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) == 12

def test_19_health_and_readiness_endpoints(client):
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "UP"

    r_ready = client.get("/readiness")
    assert r_ready.status_code == 200
    assert r_ready.json()["status"] == "READY"
