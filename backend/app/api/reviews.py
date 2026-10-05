import uuid
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.schema import Recommendation, Review, Area, User
from app.models.pydantic_models import ReviewRequest, ReviewResponse, RecommendationResponse
from app.core.auth import get_current_user, require_role

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/approve", response_model=ReviewResponse)
def submit_review(
    req: ReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submits a clinical or administrative review decision for a pending recommendation.

    Security & RBAC Enforcement:
      - Authenticated user identity derived strictly from JWT token (reviewer_id & reviewer_role).
      - OVERRIDDEN decisions require ADMIN role (CLINICIAN receives HTTP 403 Forbidden).
      - OVERRIDDEN decisions require documented justification (min 5 chars).
      - Validates modified capacity (>0) and travel distance (>=0), returning 422 on invalid values.
      - Atomic status update prevents race conditions (returns HTTP 409 Conflict if already reviewed).
    """
    # 1. Input Validation
    if req.decision not in ["ACCEPTED", "MODIFIED", "REJECTED", "OVERRIDDEN"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid review decision: '{req.decision}'. Allowed values: ACCEPTED, MODIFIED, REJECTED, OVERRIDDEN."
        )

    if req.modified_capacity is not None and req.modified_capacity <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="modified_capacity must be a positive integer strictly greater than 0."
        )

    if req.modified_travel_km is not None and req.modified_travel_km < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="modified_travel_km must be a non-negative number."
        )

    # 2. RBAC & Decision Authorization Rules
    if req.decision == "OVERRIDDEN":
        if current_user.role != "ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Clinicians are not authorized to perform hard-constraint overrides. Admin authorization required."
            )
        if not req.override_reason or len(req.override_reason.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Overriding a hard constraint requires a documented justification reason (min 5 characters)."
            )

    # 3. Check existing recommendation existence and state transition validity
    rec = db.query(Recommendation).filter(Recommendation.recommendation_id == req.recommendation_id).first()
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )

    if rec.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Recommendation '{req.recommendation_id}' has already been finalized with status '{rec.status}'."
        )

    # 4. Atomic Concurrency Control (Prevent Race Conditions)
    new_reach = req.modified_capacity if (req.modified_capacity and req.decision == "MODIFIED") else rec.expected_reach

    updated_rows = db.query(Recommendation).filter(
        Recommendation.recommendation_id == req.recommendation_id,
        Recommendation.status == "PENDING"
    ).update(
        {
            Recommendation.status: req.decision,
            Recommendation.expected_reach: new_reach
        },
        synchronize_session=False
    )

    if updated_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Concurrent review conflict: recommendation was finalized by another simultaneous user session."
        )

    # 5. Immutable Audit Trail Persistence
    review_id = str(uuid.uuid4())
    now = datetime.utcnow()

    review_entry = Review(
        review_id=review_id,
        recommendation_id=req.recommendation_id,
        reviewer_id=current_user.username,
        reviewer_role=current_user.role,
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
        reviewer_id=current_user.username,
        reviewer_role=current_user.role,
        decision=req.decision,
        override_reason=req.override_reason,
        timestamp=now.isoformat()
    )

@router.get("/audit-trail", response_model=List[ReviewResponse])
def get_audit_trail(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns the complete, append-only historical audit trail of all clinical and administrative reviews.
    """
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
def get_recommendations(
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lists recommendations filtered optionally by status.
    """
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
