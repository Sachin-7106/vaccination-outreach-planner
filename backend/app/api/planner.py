import json
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.schema import Area, ServiceHistory, DiseaseRisk, MobilityPattern, Recommendation
from app.models.pydantic_models import PlanRequest, RecommendationResponse, PlanComparisonResponse
from app.planner.baseline import calculate_baseline_scores
from app.planner.reach_engine import calculate_reach_scores
from app.planner.risk_engine import calculate_risk_scores
from app.planner.constraints import evaluate_constraints
from app.planner.explainability import generate_recommendation_reason

router = APIRouter(prefix="/planner", tags=["Planner"])

def fetch_enriched_areas_data(db: Session):
    """
    Joins Area entities with historical service records, surveillance risk signals,
    and transit mobility indicators to construct complete candidate feature vectors.
    """
    areas = db.query(Area).all()
    areas_data = []
    for area in areas:
        hist = db.query(ServiceHistory).filter(ServiceHistory.area_id == area.area_id).first()
        risk = db.query(DiseaseRisk).filter(DiseaseRisk.area_id == area.area_id).first()
        mobility = db.query(MobilityPattern).filter(MobilityPattern.area_id == area.area_id).first()

        areas_data.append({
            "area_id": area.area_id,
            "area_name": area.area_name,
            "zone_type": area.zone_type,
            "population": area.population,
            "eligible_population": area.eligible_population,
            "accessibility_index": area.accessibility_index,
            "latitude": area.latitude,
            "longitude": area.longitude,
            "distance_from_base_km": area.distance_from_base_km,
            "vaccinated_count": hist.vaccinated_count if hist else 0,
            "historical_demand": hist.historical_demand if hist else 0,
            "seasonal_risk": risk.seasonal_risk if risk else 0.0,
            "emerging_risk": risk.emerging_risk if risk else 0.0,
            "mobility_index": mobility.mobility_index if mobility else 0.0
        })
    return areas_data

@router.post("/generate", response_model=List[RecommendationResponse])
def generate_outreach_plan(req: PlanRequest, db: Session = Depends(get_db)):
    """
    Generates a targeted seasonal outreach plan for the specified objective.

    Process Flow:
      1. Aggregates zone indicators across database tables.
      2. Computes priority scores using the selected planner engine (BASELINE, REACH, or RISK).
      3. Evaluates hard/soft operational constraints (travel limits, session supply cap).
      4. Generates 100% explainable human-readable factor score breakdowns.
      5. Persists recommendation records to SQLite database for audit and human review.
    """
    areas_data = fetch_enriched_areas_data(db)
    area_lookup = {a["area_id"]: a for a in areas_data}

    if req.objective == "HISTORICAL_BASELINE":
        scored = calculate_baseline_scores(areas_data)
    elif req.objective == "MAX_REACH":
        scored = calculate_reach_scores(areas_data, w_pop=req.reach_weight_pop, w_gap=req.reach_weight_gap, w_access=req.reach_weight_access)
    else:  # RISK_REDUCTION (default)
        scored = calculate_risk_scores(areas_data, v_risk=req.risk_weight_risk, v_gap=req.risk_weight_gap, v_mobility=req.risk_weight_mobility, v_pop=req.risk_weight_pop)

    # Refresh recommendations for the requested planning period and objective
    db.query(Recommendation).filter(
        Recommendation.planning_period == req.planning_period,
        Recommendation.objective == req.objective
    ).delete()

    responses = []
    for item in scored[:req.num_sessions]:
        area_id = item["area_id"]
        area_dict = area_lookup[area_id]

        hard_passed, flags, expected_reach = evaluate_constraints(
            area_dict, req.session_capacity, req.max_travel_distance_km
        )

        reason_struct = generate_recommendation_reason(area_dict, item, req.objective)
        rec_id = str(uuid.uuid4())

        rec_db = Recommendation(
            recommendation_id=rec_id,
            area_id=area_id,
            planning_period=req.planning_period,
            objective=req.objective,
            priority_score=item["priority_score"],
            rank=item["rank"],
            expected_reach=expected_reach,
            reason=json.dumps(reason_struct),
            hard_constraint_passed=hard_passed,
            constraint_flags=json.dumps(flags),
            status="PENDING"
        )
        db.add(rec_db)

        responses.append(RecommendationResponse(
            recommendation_id=rec_id,
            area_id=area_id,
            area_name=area_dict["area_name"],
            zone_type=area_dict["zone_type"],
            planning_period=req.planning_period,
            objective=req.objective,
            priority_score=item["priority_score"],
            rank=item["rank"],
            expected_reach=expected_reach,
            distance_from_base_km=area_dict["distance_from_base_km"],
            hard_constraint_passed=hard_passed,
            constraint_flags=flags,
            status="PENDING",
            reason=reason_struct
        ))

    db.commit()
    return responses

@router.post("/compare", response_model=List[PlanComparisonResponse])
def compare_objectives(req: PlanRequest, db: Session = Depends(get_db)):
    """
    Computes a side-by-side comparison matrix across all three planning engines.

    Allows clinical decision-makers to visualize rank shifts (e.g. how high-risk zones
    ranked low in historical baselines are elevated by the Emerging Risk Engine).
    """
    areas_data = fetch_enriched_areas_data(db)

    baseline_scored = {x["area_id"]: x for x in calculate_baseline_scores(areas_data)}
    reach_scored = {x["area_id"]: x for x in calculate_reach_scores(areas_data, w_pop=req.reach_weight_pop, w_gap=req.reach_weight_gap, w_access=req.reach_weight_access)}
    risk_scored = {x["area_id"]: x for x in calculate_risk_scores(areas_data, v_risk=req.risk_weight_risk, v_gap=req.risk_weight_gap, v_mobility=req.risk_weight_mobility, v_pop=req.risk_weight_pop)}

    comparison = []
    for area in areas_data:
        aid = area["area_id"]
        b_item = baseline_scored.get(aid, {})
        r_item = reach_scored.get(aid, {})
        k_item = risk_scored.get(aid, {})

        b_rank = b_item.get("rank", 99)
        k_rank = k_item.get("rank", 99)

        comparison.append(PlanComparisonResponse(
            area_id=aid,
            area_name=area["area_name"],
            baseline_rank=b_rank,
            baseline_score=b_item.get("priority_score"),
            reach_rank=r_item.get("rank"),
            reach_score=r_item.get("priority_score"),
            risk_rank=k_rank,
            risk_score=k_item.get("priority_score"),
            historical_demand=area["historical_demand"],
            emerging_risk=area["emerging_risk"],
            eligible_population=area["eligible_population"],
            rank_difference=b_rank - k_rank  # Positive rank_difference indicates risk engine prioritized zone higher
        ))

    # Sort comparison table by emerging risk rank
    comparison.sort(key=lambda x: x.risk_rank if x.risk_rank else 99)
    return comparison
