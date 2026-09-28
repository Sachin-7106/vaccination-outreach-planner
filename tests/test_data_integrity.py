import pytest
from pydantic import ValidationError
from app.models.schema import Area, ServiceHistory, DiseaseRisk, MobilityPattern
from app.models.pydantic_models import PlanRequest, ReviewRequest

def test_db_schema_relationships(db_session):
    area = db_session.query(Area).filter(Area.area_id == "AREA-01").first()
    assert area is not None
    assert area.area_name == "Metro Central Corridor"
    assert len(area.service_histories) >= 1
    assert len(area.disease_risks) >= 1
    assert len(area.mobility_patterns) >= 1

    # Check back populate relationship
    hist = area.service_histories[0]
    assert hist.area.area_id == "AREA-01"

def test_plan_request_pydantic_validation():
    # Valid PlanRequest
    req = PlanRequest(num_sessions=5, session_capacity=300, objective="RISK_REDUCTION")
    assert req.num_sessions == 5
    assert req.session_capacity == 300

    # Invalid num_sessions (0 < 1 min)
    with pytest.raises(ValidationError):
        PlanRequest(num_sessions=0)

    # Invalid session capacity (> 2000 max)
    with pytest.raises(ValidationError):
        PlanRequest(session_capacity=5000)

    # Invalid max travel distance (> 50 km max)
    with pytest.raises(ValidationError):
        PlanRequest(max_travel_distance_km=100.0)

def test_review_request_fields():
    req = ReviewRequest(
        recommendation_id="REC-123",
        decision="ACCEPTED"
    )
    assert req.reviewer_id == "P.Officer-402"
    assert req.decision == "ACCEPTED"
