import numpy as np

def calculate_risk_scores(areas_data, v_risk=0.50, v_gap=0.25, v_mobility=0.15, v_pop=0.10):
    """
    Objective B — Emerging Risk Reduction Engine:

    Prioritizes city zones facing sudden infectious disease velocity spikes, large unvaccinated
    service gaps, high transit mobility corridors, and eligible population pools.
    Unlike historical baseline models, this proactive approach redirects outreach to emerging outbreak epicenters.

    Mathematical Formulation:
      Composite Score = (v_risk * emerging_risk) + (v_gap * service_gap) + 
                        (v_mobility * mobility_index) + (v_pop * norm_eligible_pop)
      Final Priority Score = Min-Max Normalization of Composite Score across candidate zones.
    """
    if not areas_data:
        return []

    # Extract surveillance risk velocity, service gaps, mobility patterns, and population pools
    risks = np.array([item["emerging_risk"] for item in areas_data], dtype=float)
    gaps = np.array([1.0 - (item["vaccinated_count"] / item["eligible_population"]) if item["eligible_population"] > 0 else 0.0 for item in areas_data], dtype=float)
    mobilities = np.array([item["mobility_index"] for item in areas_data], dtype=float)
    pops = np.array([item["eligible_population"] for item in areas_data], dtype=float)

    # Normalize population to [0.0, 1.0] so absolute numbers remain on a comparable scale with risk percentages
    p_min, p_max = pops.min(), pops.max()
    p_norm = (pops - p_min) / (p_max - p_min) if p_max > p_min else np.ones_like(pops)

    # Calculate raw multi-factor risk score
    raw_scores = (v_risk * risks) + (v_gap * gaps) + (v_mobility * mobilities) + (v_pop * p_norm)

    # Normalize overall score to [0.0, 1.0] for direct comparison against Reach and Baseline engines
    s_min, s_max = raw_scores.min(), raw_scores.max()
    final_scores = (raw_scores - s_min) / (s_max - s_min) if s_max > s_min else np.ones_like(raw_scores)

    results = []
    for idx, item in enumerate(areas_data):
        results.append({
            "area_id": item["area_id"],
            "area_name": item["area_name"],
            "priority_score": round(float(final_scores[idx]), 4),
            "factors": {
                "emerging_risk": round(float(risks[idx]), 4),
                "service_gap_ratio": round(float(gaps[idx]), 4),
                "mobility_index": round(float(mobilities[idx]), 4),
                "norm_eligible_pop": round(float(p_norm[idx]), 4),
                "weights": {"risk": v_risk, "gap": v_gap, "mobility": v_mobility, "pop": v_pop}
            },
            "objective": "RISK_REDUCTION"
        })

    # Rank zones in descending order of emerging risk priority
    results.sort(key=lambda x: x["priority_score"], reverse=True)
    for rank, res in enumerate(results, start=1):
        res["rank"] = rank

    return results
