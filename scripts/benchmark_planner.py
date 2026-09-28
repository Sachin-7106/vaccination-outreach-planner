import time
import numpy as np
import statistics
from app.data.seed_data import SEED_AREAS
from app.planner.baseline import calculate_baseline_scores
from app.planner.reach_engine import calculate_reach_scores
from app.planner.risk_engine import calculate_risk_scores
from app.planner.constraints import evaluate_constraints

def run_performance_benchmark(iterations=1000):
    """
    Performance Benchmark Script for City Health Vaccination Outreach Planner.
    Measures sub-millisecond execution times for scoring engines and constraint evaluation
    across synthetic city zone datasets.
    """
    print("==================================================")
    print("CITY HEALTH PLANNER — PERFORMANCE BENCHMARK")
    print("==================================================")
    print(f"Dataset Size: {len(SEED_AREAS)} City Zones")
    print(f"Iterations per Objective: {iterations:,}")
    print("--------------------------------------------------")

    objectives = [
        ("HISTORICAL_BASELINE", lambda data: calculate_baseline_scores(data)),
        ("MAX_REACH", lambda data: calculate_reach_scores(data)),
        ("RISK_REDUCTION", lambda data: calculate_risk_scores(data))
    ]

    results_summary = {}

    for name, scoring_fn in objectives:
        durations_ms = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            scored = scoring_fn(SEED_AREAS)
            # Evaluate constraints for top 5 sessions
            for item in scored[:5]:
                area = next(a for a in SEED_AREAS if a["area_id"] == item["area_id"])
                evaluate_constraints(area, session_capacity=300, max_travel_distance_km=12.0)
            t1 = time.perf_counter()
            durations_ms.append((t1 - t0) * 1000.0)

        avg_time = statistics.mean(durations_ms)
        min_time = min(durations_ms)
        max_time = max(durations_ms)
        p95_time = np.percentile(durations_ms, 95)

        results_summary[name] = {
            "avg_ms": round(avg_time, 4),
            "min_ms": round(min_time, 4),
            "max_ms": round(max_time, 4),
            "p95_ms": round(p95_time, 4)
        }

        print(f"Objective: {name}")
        print(f"  Avg Execution Time : {avg_time:.4f} ms")
        print(f"  Min Execution Time : {min_time:.4f} ms")
        print(f"  Max Execution Time : {max_time:.4f} ms")
        print(f"  P95 Execution Time : {p95_time:.4f} ms")
        print("--------------------------------------------------")

    return results_summary

if __name__ == "__main__":
    run_performance_benchmark(iterations=1000)
