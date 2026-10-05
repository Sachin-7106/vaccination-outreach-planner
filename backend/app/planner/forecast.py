import numpy as np
from typing import List, Dict, Any, Tuple

def compute_exponential_smoothing_forecast(
    historical_series: List[float],
    alpha: float = 0.4
) -> Tuple[float, str, float]:
    """
    Computes single exponential smoothing forecast for historical series.
    Returns (forecast_value, trend_direction, confidence_level).
    """
    if not historical_series:
        return 0.0, "STABLE", 0.50

    s_t = historical_series[0]
    for val in historical_series[1:]:
        s_t = alpha * val + (1 - alpha) * s_t

    if len(historical_series) >= 2:
        diff = historical_series[-1] - historical_series[0]
        if diff > 0.05:
            trend = "UPWARD"
        elif diff < -0.05:
            trend = "DOWNWARD"
        else:
            trend = "STABLE"
    else:
        trend = "STABLE"

    variance = float(np.var(historical_series)) if len(historical_series) > 1 else 0.01
    confidence = max(0.50, min(0.95, round(1.0 - (variance / (np.mean(historical_series) + 1e-5)), 2)))

    return round(s_t, 3), trend, confidence

def generate_multi_period_forecast(
    areas_data: List[Dict[str, Any]],
    target_periods: List[str] = ["2027-Q1", "2027-Q2"]
) -> List[Dict[str, Any]]:
    """
    Generates transparent multi-period demand and disease risk forecasts for all city zones.

    Methodology:
      - Exponential Smoothing (alpha = 0.4) combined with mobility trend adjustments.
      - Calculates expected demand (doses required) and projected disease risk.
      - Provides trend direction (UPWARD, STABLE, DOWNWARD) and confidence index.
    """
    forecast_results = []

    for area in areas_data:
        aid = area["area_id"]
        aname = area["area_name"]
        hist_demand = area.get("historical_demand", 200)
        curr_risk = area.get("emerging_risk", 0.5)
        mobility = area.get("mobility_index", 0.5)
        elig = area.get("eligible_population", 2000)
        vacc = area.get("vaccinated_count", 1000)
        unvacc = max(0, elig - vacc)

        # Synthetic historical trend series constructed from historical observations
        demand_history = [
            float(hist_demand * 0.85),
            float(hist_demand * 0.92),
            float(hist_demand)
        ]

        risk_history = [
            float(max(0.1, curr_risk - 0.15)),
            float(max(0.1, curr_risk - 0.05)),
            float(curr_risk)
        ]

        demand_fc, demand_trend, demand_conf = compute_exponential_smoothing_forecast(demand_history, alpha=0.4)
        risk_fc, risk_trend, risk_conf = compute_exponential_smoothing_forecast(risk_history, alpha=0.4)

        # Apply mobility adjustment to future risk forecast
        adjusted_risk_q1 = min(1.0, round(risk_fc * (1.0 + 0.1 * (mobility - 0.5)), 2))
        adjusted_risk_q2 = min(1.0, round(adjusted_risk_q1 * (1.0 + 0.05 * (mobility - 0.5)), 2))

        forecast_results.append({
            "area_id": aid,
            "area_name": aname,
            "zone_type": area["zone_type"],
            "historical_baseline_demand": hist_demand,
            "current_emerging_risk": curr_risk,
            "unvaccinated_pool": unvacc,
            "forecasts": [
                {
                    "planning_period": target_periods[0],
                    "forecast_demand_doses": int(round(demand_fc * 1.05)),
                    "forecast_disease_risk": adjusted_risk_q1,
                    "demand_trend": demand_trend,
                    "risk_trend": risk_trend,
                    "confidence_score": demand_conf
                },
                {
                    "planning_period": target_periods[1],
                    "forecast_demand_doses": int(round(demand_fc * 1.12)),
                    "forecast_disease_risk": adjusted_risk_q2,
                    "demand_trend": demand_trend,
                    "risk_trend": risk_trend,
                    "confidence_score": max(0.50, round(demand_conf - 0.05, 2))
                }
            ],
            "forecasting_method": "Single Exponential Smoothing (alpha=0.4) with Transit Mobility Factor"
        })

    return forecast_results
