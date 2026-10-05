from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class AreaBase(BaseModel):
    area_id: str
    area_name: str
    zone_type: str
    population: int
    eligible_population: int
    accessibility_index: float
    latitude: float
    longitude: float
    distance_from_base_km: float

class AreaDetail(AreaBase):
    vaccinated_count: int
    vaccination_coverage: float
    service_gap_ratio: float
    historical_demand: int
    seasonal_risk: float
    emerging_risk: float
    mobility_index: float
    inflow_index: float
    outflow_index: float

    class Config:
        from_attributes = True

class PlanRequest(BaseModel):
    planning_period: str = Field(default="2026-Q4", description="Target planning period")
    num_sessions: int = Field(default=5, ge=1, le=20, description="Available outreach sessions")
    session_capacity: int = Field(default=300, ge=50, le=2000, description="Capacity per outreach session")
    max_travel_distance_km: float = Field(default=12.0, ge=1.0, le=50.0, description="Max allowed travel distance from base")
    objective: str = Field(default="RISK_REDUCTION", description="MAX_REACH, RISK_REDUCTION, or HISTORICAL_BASELINE")
    reach_weight_pop: float = Field(default=0.45)
    reach_weight_gap: float = Field(default=0.35)
    reach_weight_access: float = Field(default=0.20)
    risk_weight_risk: float = Field(default=0.50)
    risk_weight_gap: float = Field(default=0.25)
    risk_weight_mobility: float = Field(default=0.15)
    risk_weight_pop: float = Field(default=0.10)

class ConstraintFlag(BaseModel):
    code: str
    severity: str  # HARD or SOFT
    message: str

class RecommendationResponse(BaseModel):
    recommendation_id: str
    area_id: str
    area_name: str
    zone_type: str
    planning_period: str
    objective: str
    priority_score: float
    rank: int
    expected_reach: int
    distance_from_base_km: float
    hard_constraint_passed: bool
    constraint_flags: List[ConstraintFlag]
    status: str
    reason: Dict[str, Any]

class PlanComparisonResponse(BaseModel):
    area_id: str
    area_name: str
    baseline_rank: Optional[int] = None
    baseline_score: Optional[float] = None
    reach_rank: Optional[int] = None
    reach_score: Optional[float] = None
    risk_rank: Optional[int] = None
    risk_score: Optional[float] = None
    historical_demand: int
    emerging_risk: float
    eligible_population: int
    rank_difference: int  # Difference between Baseline and Risk score rank

class ReviewRequest(BaseModel):
    recommendation_id: str
    decision: str  # ACCEPTED, MODIFIED, REJECTED, OVERRIDDEN
    override_reason: Optional[str] = None
    modified_capacity: Optional[int] = None
    modified_travel_km: Optional[float] = None
    reviewer_id: Optional[str] = "P.Officer-402"
    reviewer_role: Optional[str] = "Public Health Reviewer"

class ReviewResponse(BaseModel):
    review_id: str
    recommendation_id: str
    reviewer_id: str
    reviewer_role: str
    decision: str
    override_reason: Optional[str]
    timestamp: str

class EvalMetricsResponse(BaseModel):
    objective: str
    eligible_reached_per_session: float
    total_eligible_reached: int
    total_capacity_allocated: int
    session_utilisation_rate: float
    unmet_eligible_demand: int
    areas_served_count: int
    risk_weighted_coverage_score: float
    travel_feasibility_rate: float

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    role: str
    full_name: str

class TokenData(BaseModel):
    username: str
    role: str

class UserResponse(BaseModel):
    user_id: str
    username: str
    role: str
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True

