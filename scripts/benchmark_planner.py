import time
import statistics
import numpy as np
from app.data.seed_data import SEED_AREAS
from app.planner.baseline import calculate_baseline_scores
from app.planner.reach_engine import calculate_reach_scores
from app.planner.risk_engine import calculate_risk_scores
from app.planner.constraints import evaluate_constraints
from app.planner.optimizer import solve_outreach_allocation
from app.planner.forecast import generate_multi_period_forecast

def run_performance_benchmark(iterations=500):
    """
    Comprehensive Performance Benchmark Script for City Health Vaccination Outreach Planner.
    Measures sub-millisecond and millisecond execution times across:
      - Statistical Scoring Engines
      - Formal PuLP CBC Integer Linear Programming (ILP) Optimizer
      - Multi-Period Forecasting Engine
      - Operational Constraint Evaluation
    """
    print("==================================================")
    print("CITY HEALTH PLANNER — COMPREHENSIVE BENCHMARK")
    print("==================================================")
    print(f"Dataset Size: {len(SEED_AREAS)} Synthetic City Zones")
    print(f"Iterations per Benchmark Component: {iterations:,}")
    print("--------------------------------------------------")

    benchmark_tasks = [
        ("RISK_REDUCTION_SCORING", lambda data: calculate_risk_scores(data)),
        ("REACH_SCORING", lambda data: calculate_reach_scores(data)),
        ("BASELINE_SCORING", lambda data: calculate_baseline_scores(data)),
        ("ILP_OPTIMIZER_CBC", lambda data: solve_outreach_allocation(
            areas_data=data,
            scored_items=calculate_risk_scores(data),
            num_sessions=5,
            session_capacity=300,
            max_travel_distance_km=12.0,
            objective_type="RISK_REDUCTION"
        )),
        ("MULTI_PERIOD_FORECASTING", lambda data: generate_multi_period_forecast(data)),
        ("CONSTRAINT_EVALUATION_12_AREAS", lambda data: [
            evaluate_constraints(area, session_capacity=300, max_travel_distance_km=12.0)
            for area in data
        ])
    ]

    results_summary = {}

    for name, task_fn in benchmark_tasks:
        durations_ms = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            task_fn(SEED_AREAS)
            t1 = time.perf_counter()
            durations_ms.append((t1 - t0) * 1000.0)

        avg_time = statistics.mean(durations_ms)
        min_time = min(durations_ms)
        max_time = max(durations_ms)
        std_dev = statistics.stdev(durations_ms) if len(durations_ms) > 1 else 0.0
        p95_time = float(np.percentile(durations_ms, 95))

        results_summary[name] = {
            "avg_ms": round(avg_time, 4),
            "min_ms": round(min_time, 4),
            "max_ms": round(max_time, 4),
            "std_dev_ms": round(std_dev, 4),
            "p95_ms": round(p95_time, 4)
        }

        print(f"Component: {name}")
        print(f"  Avg Execution Time : {avg_time:.4f} ms")
        print(f"  Min Execution Time : {min_time:.4f} ms")
        print(f"  Max Execution Time : {max_time:.4f} ms")
        print(f"  Std Dev            : {std_dev:.4f} ms")
        print(f"  P95 Execution Time : {p95_time:.4f} ms")
        print("--------------------------------------------------")

    return results_summary

if __name__ == "__main__":
    run_performance_benchmark(iterations=500)
