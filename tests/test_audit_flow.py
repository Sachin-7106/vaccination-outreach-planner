import pytest
from app.core.database import Base, engine, SessionLocal
from app.models.schema import Recommendation, Review, Area
from app.api.reviews import submit_review
from app.models.pydantic_models import ReviewRequest
from fastapi import HTTPException

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

def test_override_requires_justification(db_session):
    # Setup dummy recommendation
    rec = Recommendation(
        recommendation_id="REC-TEST-99",
        area_id="AREA-01",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.85,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=False,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    # Attempt override without reason -> should raise 400 HTTPException
    req_invalid = ReviewRequest(
        recommendation_id="REC-TEST-99",
        reviewer_id="Test.Reviewer",
        reviewer_role="CLINICIAN",
        decision="OVERRIDDEN",
        override_reason=""
    )
    with pytest.raises(HTTPException) as exc_info:
        submit_review(req_invalid, db_session)
    assert exc_info.value.status_code == 400

    # Submit valid override with mandatory reason
    req_valid = ReviewRequest(
        recommendation_id="REC-TEST-99",
        reviewer_id="Test.Reviewer",
        reviewer_role="CLINICIAN",
        decision="OVERRIDDEN",
        override_reason="Authorized secondary mobile transit bus allocated"
    )
    resp = submit_review(req_valid, db_session)
    assert resp.decision == "OVERRIDDEN"
    assert resp.override_reason == "Authorized secondary mobile transit bus allocated"
