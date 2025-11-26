"""
Performance Benchmarking Script

Compares sequential vs parallel execution to measure speedup.
Run this to validate optimization improvements.

Usage:
    python benchmark_performance.py <project_path>
    python benchmark_performance.py ../student-project --runs 3
"""

import sys
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.skill_executor import run_all_skills
from src.core.skill_executor_optimized import run_all_skills_parallel


def benchmark_sequential(project_path: str) -> float:
    """Benchmark sequential execution."""
    print("\n" + "=" * 60)
    print("BENCHMARK: Sequential Execution (Original)")
    print("=" * 60)

    start = time.time()
    results = run_all_skills(project_path)
    elapsed = time.time() - start

    print(f"\n[*] Sequential completed in {elapsed:.2f}s")
    print(f"[*] Score: {results['total_score']}/100")

    return elapsed


def benchmark_parallel(project_path: str, workers: int = 4) -> float:
    """Benchmark parallel execution."""
    print("\n" + "=" * 60)
    print(f"BENCHMARK: Parallel Execution ({workers} workers)")
    print("=" * 60)

    start = time.time()
    results = run_all_skills_parallel(
        project_path,
        max_workers=workers,
        enable_early_exit=True
    )
    elapsed = time.time() - start

    print(f"\n[*] Parallel completed in {elapsed:.2f}s")
    print(f"[*] Score: {results['total_score']}/100")
    print(f"[*] Early exit: {results.get('early_exit', False)}")

    return elapsed


def main():
    """Run performance benchmarks."""
    parser = argparse.ArgumentParser(
        description='Benchmark auto-grader performance'
    )
    parser.add_argument('project_path', help='Path to project to grade')
    parser.add_argument(
        '--runs',
        type=int,
        default=1,
        help='Number of benchmark runs (default: 1)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Parallel workers (default: 4)'
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("AUTO-GRADER PERFORMANCE BENCHMARK")
    print("=" * 60)
    print(f"Project: {args.project_path}")
    print(f"Runs: {args.runs}")
    print(f"Workers: {args.workers}")

    sequential_times = []
    parallel_times = []

    for run in range(args.runs):
        print(f"\n\n{'#' * 60}")
        print(f"RUN {run + 1}/{args.runs}")
        print('#' * 60)

        # Benchmark sequential
        seq_time = benchmark_sequential(args.project_path)
        sequential_times.append(seq_time)

        # Small delay between runs
        time.sleep(1)

        # Benchmark parallel
        par_time = benchmark_parallel(args.project_path, args.workers)
        parallel_times.append(par_time)

    # Calculate statistics
    avg_sequential = sum(sequential_times) / len(sequential_times)
    avg_parallel = sum(parallel_times) / len(parallel_times)
    speedup = avg_sequential / avg_parallel
    time_saved = avg_sequential - avg_parallel
    percent_faster = ((avg_sequential - avg_parallel) / avg_sequential) * 100

    # Display results
    print("\n\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(f"\nSequential (Original):")
    print(f"  Average time: {avg_sequential:.2f}s")
    if args.runs > 1:
        print(f"  Min: {min(sequential_times):.2f}s")
        print(f"  Max: {max(sequential_times):.2f}s")

    print(f"\nParallel (Optimized, {args.workers} workers):")
    print(f"  Average time: {avg_parallel:.2f}s")
    if args.runs > 1:
        print(f"  Min: {min(parallel_times):.2f}s")
        print(f"  Max: {max(parallel_times):.2f}s")

    print(f"\nPerformance Improvement:")
    print(f"  Speedup: {speedup:.2f}x")
    print(f"  Time saved: {time_saved:.2f}s")
    print(f"  Faster by: {percent_faster:.1f}%")

    # Interpretation
    print("\n" + "-" * 60)
    if speedup >= 3.0:
        print("🚀 EXCELLENT: Major performance improvement!")
    elif speedup >= 2.0:
        print("✅ GOOD: Significant speedup achieved")
    elif speedup >= 1.5:
        print("👍 MODERATE: Noticeable improvement")
    else:
        print("⚠️  LIMITED: Small improvement (I/O bound or overhead)")

    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
