import numpy as np

def calculate_baseline_scores(areas_data):
    """
    Historical Average Baseline Model:
    
    Calculates priority scores based on past session attendance history relative
    to eligible population. Serves as the benchmark model to demonstrate how
    legacy historical allocation policies miss emerging disease spikes.
    
    Mathematical Formulation:
      Raw Score = Historical Demand / Eligible Population
      Normalized Score = Min-Max Normalization to scale values into [0.0, 1.0]
    """
    if not areas_data:
        return []

    scores = []
    for item in areas_data:
        elig = item["eligible_population"]
        hist_demand = item["historical_demand"]
        
        # Raw baseline score: ratio of historical demand to eligible pop
        raw_score = (hist_demand / elig) if elig > 0 else 0.0
        scores.append(raw_score)
    
    # Min-max normalization for direct comparison across models
    scores = np.array(scores, dtype=float)
    min_val, max_val = scores.min(), scores.max()
    if max_val > min_val:
        norm_scores = (scores - min_val) / (max_val - min_val)
    else:
        norm_scores = np.ones_like(scores)

    results = []
    for idx, item in enumerate(areas_data):
        results.append({
            "area_id": item["area_id"],
            "area_name": item["area_name"],
            "priority_score": round(float(norm_scores[idx]), 4),
            "raw_score": round(float(scores[idx]), 4),
            "historical_demand": item["historical_demand"],
            "objective": "HISTORICAL_BASELINE"
        })
    
    # Sort descending by score
    results.sort(key=lambda x: x["priority_score"], reverse=True)
    for rank, res in enumerate(results, start=1):
        res["rank"] = rank

    return results
