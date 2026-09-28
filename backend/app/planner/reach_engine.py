import numpy as np

def calculate_reach_scores(areas_data, w_pop=0.45, w_gap=0.35, w_access=0.20):
    """
    Objective A — Maximum Eligible Reach Engine:

    Prioritizes city zones with large vulnerable population pools, high un-vaccinated
    service gaps, and favorable geographic accessibility to maximize aggregate vaccine uptake.

    Mathematical Formulation:
      1. Normalize population (p_norm) to [0.0, 1.0] so absolute population scale is comparable with ratios.
      2. Service gap ratio = 1.0 - (vaccinated / eligible).
      3. Composite Score = (w_pop * p_norm) + (w_gap * service_gap) + (w_access * accessibility_index)
      4. Final Priority Score = Min-Max Normalization of Composite Score across all candidate zones.
    """
    if not areas_data:
        return []

    # Extract target population pools, unvaccinated gap ratios, and access indices
    pops = np.array([item["eligible_population"] for item in areas_data], dtype=float)
    gaps = np.array([1.0 - (item["vaccinated_count"] / item["eligible_population"]) if item["eligible_population"] > 0 else 0.0 for item in areas_data], dtype=float)
    access = np.array([item["accessibility_index"] for item in areas_data], dtype=float)

    # Normalize population to [0.0, 1.0] to prevent huge population numbers from overwhelming ratio metrics
    p_min, p_max = pops.min(), pops.max()
    p_norm = (pops - p_min) / (p_max - p_min) if p_max > p_min else np.ones_like(pops)

    # Compute raw multi-objective weighted combination
    raw_scores = w_pop * p_norm + w_gap * gaps + w_access * access

    # Min-max normalize final scores to ensure consistent [0.0, 1.0] range across different objectives
    s_min, s_max = raw_scores.min(), raw_scores.max()
    final_scores = (raw_scores - s_min) / (s_max - s_min) if s_max > s_min else np.ones_like(raw_scores)

    results = []
    for idx, item in enumerate(areas_data):
        results.append({
            "area_id": item["area_id"],
            "area_name": item["area_name"],
            "priority_score": round(float(final_scores[idx]), 4),
            "factors": {
                "norm_eligible_pop": round(float(p_norm[idx]), 4),
                "service_gap_ratio": round(float(gaps[idx]), 4),
                "accessibility_index": round(float(access[idx]), 4),
                "weights": {"pop": w_pop, "gap": w_gap, "access": w_access}
            },
            "objective": "MAX_REACH"
        })

    # Sort descending by priority score and assign 1-based ranks
    results.sort(key=lambda x: x["priority_score"], reverse=True)
    for rank, res in enumerate(results, start=1):
        res["rank"] = rank

    return results
