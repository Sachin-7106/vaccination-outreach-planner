import pytest
from app.models.schema import Recommendation, Review, User
from app.api.reviews import submit_review
from app.models.pydantic_models import ReviewRequest
from fastapi import HTTPException

def test_override_requires_justification(db_session):
    admin_user = User(
        user_id="usr-admin-test",
        username="Test.Reviewer",
        role="ADMIN",
        full_name="System Admin",
        is_active=True
    )

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

    req_invalid = ReviewRequest(
        recommendation_id="REC-TEST-99",
        reviewer_id="Test.Reviewer",
        reviewer_role="ADMIN",
        decision="OVERRIDDEN",
        override_reason=""
    )
    with pytest.raises(HTTPException) as exc_info:
        submit_review(req_invalid, db_session, current_user=admin_user)
    assert exc_info.value.status_code == 400
    assert "justification" in exc_info.value.detail.lower()

    req_valid = ReviewRequest(
        recommendation_id="REC-TEST-99",
        reviewer_id="Test.Reviewer",
        reviewer_role="ADMIN",
        decision="OVERRIDDEN",
        override_reason="Authorized secondary mobile transit bus allocated"
    )
    resp = submit_review(req_valid, db_session, current_user=admin_user)
    assert resp.decision == "OVERRIDDEN"
    assert resp.override_reason == "Authorized secondary mobile transit bus allocated"

    db_rec = db_session.query(Recommendation).filter_by(recommendation_id="REC-TEST-99").first()
    assert db_rec.status == "OVERRIDDEN"

    db_review = db_session.query(Review).filter_by(recommendation_id="REC-TEST-99").first()
    assert db_review is not None
    assert db_review.reviewer_id == "Test.Reviewer"
