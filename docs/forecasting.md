# Multi-Period Demand & Disease Risk Forecasting

## Overview
The Vaccination Outreach Planner incorporates a transparent, explainable multi-period forecasting module to anticipate future seasonal demand spikes and emerging disease risk across city zones.

Rather than using opaque black-box machine learning models, the system employs **Single Exponential Smoothing (SES)** combined with **Transit Mobility Factors** to project demand over upcoming planning periods (e.g., `2027-Q1`, `2027-Q2`).

---

## 1. Mathematical Formulation

### Single Exponential Smoothing Equation
For a historical time series of observed demand or disease risk signals $Y_1, Y_2, \dots, Y_t$:

$$\hat{Y}_{t+1} = \alpha Y_t + (1 - \alpha) \hat{Y}_t$$

Where:
- $\hat{Y}_{t+1}$: Forecasted value for period $t+1$.
- $Y_t$: Most recent observed metric (e.g. historical session attendance or emerging risk index).
- $\hat{Y}_t$: Previous smoothed forecast estimate.
- $\alpha = 0.4$: Smoothing factor giving balanced weight to recent signals vs historical baseline.

### Mobility Adjustment Factor
Future disease transmission risk in high-density or high-transit zones is adjusted for population movement:

$$R_{\text{forecast}, t+1} = \min\left(1.0, \, \hat{R}_{t+1} \cdot \Big(1.0 + 0.10 \times (\text{MobilityIndex} - 0.50)\Big)\right)$$

---

## 2. API Specifications

### Endpoint: `GET /api/forecast`

**Authentication**: Bearer Token required (`ADMIN` or `CLINICIAN` role).

**Query Parameters**:
- `area_id` (optional): Filter forecast results by specific area ID (e.g. `AREA-07`).

#### Example Response:

```json
[
  {
    "area_id": "AREA-07",
    "area_name": "Eastside Railway Market",
    "zone_type": "Mobile Vendor Settlement",
    "historical_baseline_demand": 95,
    "current_emerging_risk": 0.96,
    "unvaccinated_pool": 3820,
    "forecasts": [
      {
        "planning_period": "2027-Q1",
        "forecast_demand_doses": 105,
        "forecast_disease_risk": 0.98,
        "demand_trend": "UPWARD",
        "risk_trend": "UPWARD",
        "confidence_score": 0.88
      },
      {
        "planning_period": "2027-Q2",
        "forecast_demand_doses": 112,
        "forecast_disease_risk": 1.00,
        "demand_trend": "UPWARD",
        "risk_trend": "UPWARD",
        "confidence_score": 0.83
      }
    ],
    "forecasting_method": "Single Exponential Smoothing (alpha=0.4) with Transit Mobility Factor"
  }
]
```

---

## 3. Scope & Limitations

1. **Synthetic Data Context**: Historical demand and disease risk signals are derived from synthetic municipal data.
2. **Deterministic Smoothing**: The exponential smoothing method is lightweight and fully deterministic. It does not claim deep learning or stochastic neural time-series capabilities.
3. **Planning Integration**: Forecast outputs serve as advisories for clinical decision-makers during multi-period resource budgeting.
