import pytest
from app.models.schema import Recommendation, Review, User
from app.api.reviews import submit_review, get_audit_trail, get_recommendations
from app.models.pydantic_models import ReviewRequest
from fastapi import HTTPException

@pytest.fixture
def mock_user():
    return User(
        user_id="usr-mock-1",
        username="clinician",
        role="CLINICIAN",
        full_name="Dr. Sarah Chen",
        is_active=True
    )

@pytest.fixture
def mock_admin():
    return User(
        user_id="usr-mock-admin",
        username="admin",
        role="ADMIN",
        full_name="System Administrator",
        is_active=True
    )

def test_submit_review_accepted(db_session, mock_user):
    rec = Recommendation(
        recommendation_id="REC-TEST-ACCEPT",
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

    req = ReviewRequest(
        recommendation_id="REC-TEST-ACCEPT",
        reviewer_id="Officer-101",
        reviewer_role="Public Health Director",
        decision="ACCEPTED"
    )
    resp = submit_review(req, db_session, current_user=mock_user)
    assert resp.decision == "ACCEPTED"
    assert resp.recommendation_id == "REC-TEST-ACCEPT"

    db_rec = db_session.query(Recommendation).filter_by(recommendation_id="REC-TEST-ACCEPT").first()
    assert db_rec.status == "ACCEPTED"

def test_submit_review_modified_capacity(db_session, mock_user):
    rec = Recommendation(
        recommendation_id="REC-TEST-MODIFY",
        area_id="AREA-02",
        planning_period="2026-Q4",
        objective="MAX_REACH",
        priority_score=0.75,
        rank=2,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=True,
        status="PENDING"
    )
    db_session.add(rec)
    db_session.commit()

    req = ReviewRequest(
        recommendation_id="REC-TEST-MODIFY",
        reviewer_id="Officer-102",
        reviewer_role="Field Lead",
        decision="MODIFIED",
        modified_capacity=150
    )
    resp = submit_review(req, db_session, current_user=mock_user)
    assert resp.decision == "MODIFIED"

    db_rec = db_session.query(Recommendation).filter_by(recommendation_id="REC-TEST-MODIFY").first()
    assert db_rec.status == "MODIFIED"
    assert db_rec.expected_reach == 150

def test_submit_review_not_found(db_session, mock_user):
    req = ReviewRequest(
        recommendation_id="NON-EXISTENT-ID",
        reviewer_id="Officer-999",
        reviewer_role="Tester",
        decision="ACCEPTED"
    )
    with pytest.raises(HTTPException) as exc_info:
        submit_review(req, db_session, current_user=mock_user)
    assert exc_info.value.status_code == 404

def test_audit_trail_retrieval(db_session, mock_user):
    rec = Recommendation(
        recommendation_id="REC-AUDIT-1",
        area_id="AREA-01",
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

    req = ReviewRequest(
        recommendation_id="REC-AUDIT-1",
        reviewer_id="Officer-Audit",
        reviewer_role="Auditor",
        decision="ACCEPTED"
    )
    submit_review(req, db_session, current_user=mock_user)

    trail = get_audit_trail(db_session, current_user=mock_user)
    assert len(trail) >= 1
    assert trail[0].reviewer_id == "clinician"

def test_get_recommendations_filtering(db_session, mock_user):
    rec1 = Recommendation(
        recommendation_id="REC-FILT-1",
        area_id="AREA-01",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.95,
        rank=1,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=True,
        status="PENDING"
    )
    rec2 = Recommendation(
        recommendation_id="REC-FILT-2",
        area_id="AREA-02",
        planning_period="2026-Q4",
        objective="RISK_REDUCTION",
        priority_score=0.85,
        rank=2,
        expected_reach=300,
        reason="{}",
        hard_constraint_passed=True,
        status="ACCEPTED"
    )
    db_session.add_all([rec1, rec2])
    db_session.commit()

    pending = get_recommendations(status="PENDING", db=db_session, current_user=mock_user)
    assert len(pending) == 1
    assert pending[0].recommendation_id == "REC-FILT-1"

    accepted = get_recommendations(status="ACCEPTED", db=db_session, current_user=mock_user)
    assert len(accepted) == 1
    assert accepted[0].recommendation_id == "REC-FILT-2"

