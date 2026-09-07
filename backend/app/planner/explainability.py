def generate_recommendation_reason(area_dict, scored_item, objective):
    """
    Generates a structured human-readable breakdown explaining why an area was selected.
    """
    elig = area_dict.get("eligible_population", 0)
    vacc = area_dict.get("vaccinated_count", 0)
    unvacc = max(0, elig - vacc)
    coverage_pct = round((vacc / elig * 100), 1) if elig > 0 else 0.0
    risk = area_dict.get("emerging_risk", 0.0)
    mobility = area_dict.get("mobility_index", 0.0)
    access = area_dict.get("accessibility_index", 0.0)
    dist = area_dict.get("distance_from_base_km", 0.0)
    hist_demand = area_dict.get("historical_demand", 0)

    factors_breakdown = []

    if objective == "RISK_REDUCTION":
        factors_breakdown = [
            {"factor": "Emerging Risk Spike", "value": f"{risk:.2f}", "impact": "High Priority" if risk > 0.7 else "Moderate"},
            {"factor": "Unvaccinated Pool", "value": f"{unvacc:,} people ({100-coverage_pct:.1f}% gap)", "impact": "High Need"},
            {"factor": "Transit Mobility Index", "value": f"{mobility:.2f}", "impact": "High Exposure" if mobility > 0.8 else "Standard"},
            {"factor": "Distance from Base", "value": f"{dist:.1f} km", "impact": "Feasible"}
        ]
        summary_text = (
            f"{area_dict['area_name']} selected for Emerging Risk Reduction due to high risk signal ({risk:.2f}) "
            f"and significant unvaccinated population ({unvacc:,} eligible)."
        )

    elif objective == "MAX_REACH":
        factors_breakdown = [
            {"factor": "Eligible Population", "value": f"{elig:,}", "impact": "High Scale"},
            {"factor": "Unvaccinated Pool", "value": f"{unvacc:,}", "impact": "High Capacity Match"},
            {"factor": "Geographic Access Index", "value": f"{access:.2f}", "impact": "Good Feasibility" if access > 0.7 else "Moderate"},
            {"factor": "Distance from Base", "value": f"{dist:.1f} km", "impact": "Feasible"}
        ]
        summary_text = (
            f"{area_dict['area_name']} selected for Maximum Eligible Reach due to large aggregate target population ({elig:,}) "
            f"and strong accessibility ({access:.2f})."
        )

    else:  # HISTORICAL_BASELINE
        factors_breakdown = [
            {"factor": "Historical Session Attendance", "value": f"{hist_demand} visits", "impact": "Past Pattern"},
            {"factor": "Eligible Population", "value": f"{elig:,}", "impact": "Baseline Ratio"}
        ]
        summary_text = (
            f"{area_dict['area_name']} selected by Historical Baseline based on past average attendance ({hist_demand} visits)."
        )

    return {
        "summary": summary_text,
        "primary_objective": objective,
        "priority_score": scored_item["priority_score"],
        "rank": scored_item["rank"],
        "factors": factors_breakdown,
        "metrics_snapshot": {
            "eligible_population": elig,
            "vaccinated_count": vacc,
            "unvaccinated_count": unvacc,
            "coverage_percentage": coverage_pct,
            "emerging_risk": risk,
            "mobility_index": mobility,
            "accessibility_index": access,
            "distance_km": dist,
            "historical_demand": hist_demand
        }
    }
