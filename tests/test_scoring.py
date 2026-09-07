import pytest
from app.planner.baseline import calculate_baseline_scores
from app.planner.reach_engine import calculate_reach_scores
from app.planner.risk_engine import calculate_risk_scores

@pytest.fixture
def sample_areas():
    return [
        {
            "area_id": "AREA-A",
            "area_name": "Historical High Area",
            "population": 10000,
            "eligible_population": 2000,
            "vaccinated_count": 1500,
            "historical_demand": 400,
            "seasonal_risk": 0.20,
            "emerging_risk": 0.15,
            "mobility_index": 0.30,
            "accessibility_index": 0.90,
            "distance_from_base_km": 3.0
        },
        {
            "area_id": "AREA-B",
            "area_name": "Emerging Risk Spike Area",
            "population": 12000,
            "eligible_population": 4000,
            "vaccinated_count": 500,  # 3500 unvaccinated
            "historical_demand": 80,   # Low historical demand!
            "seasonal_risk": 0.85,
            "emerging_risk": 0.95,  # High emerging risk spike!
            "mobility_index": 0.90,
            "accessibility_index": 0.60,
            "distance_from_base_km": 7.0
        }
    ]

def test_baseline_scores(sample_areas):
    scores = calculate_baseline_scores(sample_areas)
    assert len(scores) == 2
    # Area A should be rank 1 in historical baseline because historical_demand is 400 vs 80
    assert scores[0]["area_id"] == "AREA-A"
    assert scores[0]["rank"] == 1

def test_risk_scores_overrides_historical_baseline(sample_areas):
    scores = calculate_risk_scores(sample_areas)
    assert len(scores) == 2
    # Area B MUST be rank 1 in Risk Reduction Engine because emerging_risk is 0.95 vs 0.15
    assert scores[0]["area_id"] == "AREA-B"
    assert scores[0]["rank"] == 1
    assert scores[0]["priority_score"] > scores[1]["priority_score"]

def test_reach_scores(sample_areas):
    scores = calculate_reach_scores(sample_areas)
    assert len(scores) == 2
    # Area B has larger eligible pop (4000) and un-vaccinated gap (3500)
    assert scores[0]["area_id"] == "AREA-B"
