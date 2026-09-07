from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.api.planner import fetch_enriched_areas_data
from app.planner.baseline import calculate_baseline_scores
from app.planner.reach_engine import calculate_reach_scores
from app.planner.risk_engine import calculate_risk_scores
from app.planner.constraints import evaluate_constraints
from app.planner.explainability import generate_recommendation_reason
from app.planner.evaluator import compute_evaluation_metrics, get_error_analysis_scenarios
from app.models.pydantic_models import EvalMetricsResponse

router = APIRouter(prefix="/eval", tags=["Evaluation"])

def helper_generate_scored_list(areas_data, objective, num_sessions=5, capacity=300, max_dist=12.0):
    area_lookup = {a["area_id"]: a for a in areas_data}
    if objective == "HISTORICAL_BASELINE":
        scored = calculate_baseline_scores(areas_data)
    elif objective == "MAX_REACH":
        scored = calculate_reach_scores(areas_data)
    else:
        scored = calculate_risk_scores(areas_data)

    recs = []
    for item in scored[:num_sessions]:
        area_id = item["area_id"]
        area_dict = area_lookup[area_id]
        hard_passed, flags, expected_reach = evaluate_constraints(area_dict, capacity, max_dist)
        reason_struct = generate_recommendation_reason(area_dict, item, objective)

        recs.append({
            "area_id": area_id,
            "expected_reach": expected_reach,
            "hard_constraint_passed": hard_passed,
            "reason": reason_struct
        })
    return recs

@router.get("/metrics", response_model=List[EvalMetricsResponse])
def get_evaluation_metrics(num_sessions: int = 5, capacity: int = 300, max_dist: float = 12.0, db: Session = Depends(get_db)):
    areas_data = fetch_enriched_areas_data(db)

    baseline_recs = helper_generate_scored_list(areas_data, "HISTORICAL_BASELINE", num_sessions, capacity, max_dist)
    reach_recs = helper_generate_scored_list(areas_data, "MAX_REACH", num_sessions, capacity, max_dist)
    risk_recs = helper_generate_scored_list(areas_data, "RISK_REDUCTION", num_sessions, capacity, max_dist)

    b_eval = compute_evaluation_metrics(baseline_recs, num_sessions, capacity)
    r_eval = compute_evaluation_metrics(reach_recs, num_sessions, capacity)
    k_eval = compute_evaluation_metrics(risk_recs, num_sessions, capacity)

    return [
        EvalMetricsResponse(objective="HISTORICAL_BASELINE", **b_eval),
        EvalMetricsResponse(objective="MAX_REACH", **r_eval),
        EvalMetricsResponse(objective="RISK_REDUCTION", **k_eval)
    ]

@router.get("/error-analysis")
def get_error_analysis():
    return get_error_analysis_scenarios()
