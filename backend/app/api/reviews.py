import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.schema import Recommendation, Review, Area
from app.models.pydantic_models import ReviewRequest, ReviewResponse, RecommendationResponse
import json

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/approve", response_model=ReviewResponse)
def submit_review(req: ReviewRequest, db: Session = Depends(get_db)):
    rec = db.query(Recommendation).filter(Recommendation.recommendation_id == req.recommendation_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    # If decision is OVERRIDDEN, require explicit override reason
    if req.decision == "OVERRIDDEN" and (not req.override_reason or len(req.override_reason.strip()) < 5):
        raise HTTPException(
            status_code=400,
            detail="Overriding a hard constraint requires a documented justification reason (min 5 characters)."
        )

    # Update recommendation status
    rec.status = req.decision
    if req.modified_capacity:
        rec.expected_reach = req.modified_capacity

    review_id = str(uuid.uuid4())
    now = datetime.utcnow()

    review_entry = Review(
        review_id=review_id,
        recommendation_id=req.recommendation_id,
        reviewer_id=req.reviewer_id,
        reviewer_role=req.reviewer_role,
        decision=req.decision,
        override_reason=req.override_reason,
        modified_capacity=req.modified_capacity,
        modified_travel_km=req.modified_travel_km,
        timestamp=now
    )
    db.add(review_entry)
    db.commit()

    return ReviewResponse(
        review_id=review_id,
        recommendation_id=req.recommendation_id,
        reviewer_id=req.reviewer_id,
        reviewer_role=req.reviewer_role,
        decision=req.decision,
        override_reason=req.override_reason,
        timestamp=now.isoformat()
    )

@router.get("/audit-trail", response_model=List[ReviewResponse])
def get_audit_trail(db: Session = Depends(get_db)):
    reviews = db.query(Review).order_by(Review.timestamp.desc()).all()
    result = []
    for r in reviews:
        result.append(ReviewResponse(
            review_id=r.review_id,
            recommendation_id=r.recommendation_id,
            reviewer_id=r.reviewer_id,
            reviewer_role=r.reviewer_role,
            decision=r.decision,
            override_reason=r.override_reason,
            timestamp=r.timestamp.isoformat() if r.timestamp else datetime.utcnow().isoformat()
        ))
    return result

@router.get("/recommendations", response_model=List[RecommendationResponse])
def get_recommendations(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Recommendation)
    if status:
        query = query.filter(Recommendation.status == status)
    recs = query.order_by(Recommendation.rank.asc()).all()

    results = []
    for r in recs:
        area = db.query(Area).filter(Area.area_id == r.area_id).first()
        reason_struct = json.loads(r.reason) if r.reason else {}
        flags_struct = json.loads(r.constraint_flags) if r.constraint_flags else []

        results.append(RecommendationResponse(
            recommendation_id=r.recommendation_id,
            area_id=r.area_id,
            area_name=area.area_name if area else r.area_id,
            zone_type=area.zone_type if area else "Zone",
            planning_period=r.planning_period,
            objective=r.objective,
            priority_score=r.priority_score,
            rank=r.rank,
            expected_reach=r.expected_reach,
            distance_from_base_km=area.distance_from_base_km if area else 0.0,
            hard_constraint_passed=r.hard_constraint_passed,
            constraint_flags=flags_struct,
            status=r.status,
            reason=reason_struct
        ))
    return results
