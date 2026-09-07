import numpy as np

def calculate_reach_scores(areas_data, w_pop=0.45, w_gap=0.35, w_access=0.20):
    """
    Objective A — Maximum Eligible Reach:
    Focuses on large eligible populations, un-vaccinated service gaps, and high geographic access.
    """
    if not areas_data:
        return []

    pops = np.array([item["eligible_population"] for item in areas_data], dtype=float)
    gaps = np.array([1.0 - (item["vaccinated_count"] / item["eligible_population"]) if item["eligible_population"] > 0 else 0.0 for item in areas_data], dtype=float)
    access = np.array([item["accessibility_index"] for item in areas_data], dtype=float)

    # Normalize population to [0, 1]
    p_min, p_max = pops.min(), pops.max()
    p_norm = (pops - p_min) / (p_max - p_min) if p_max > p_min else np.ones_like(pops)

    # Calculate weighted score
    raw_scores = w_pop * p_norm + w_gap * gaps + w_access * access

    # Min-max normalize overall score to [0, 1]
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

    results.sort(key=lambda x: x["priority_score"], reverse=True)
    for rank, res in enumerate(results, start=1):
        res["rank"] = rank

    return results
