"""Generate benchmark plots for the performance report."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

RESULTS_PATH = Path("benchmark_results.csv")
FIGURES_DIR = Path("report/figures")


def read_results() -> dict[str, list[tuple[str, float]]]:
    """Read benchmark CSV results grouped by algorithm."""
    grouped: dict[str, list[tuple[str, float]]] = defaultdict(list)
    with RESULTS_PATH.open(encoding="utf-8") as file:
        for row in csv.DictReader(file):
            label = f"{row['width']}x{row['height']}"
            grouped[row["algorithm"]].append((label, float(row["seconds"])))
    return dict(grouped)


def generate_plot() -> None:
    """Generate and save a line chart with benchmark results."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    grouped = read_results()
    plt.figure(figsize=(10, 6))
    for algorithm, values in grouped.items():
        labels = [label for label, _seconds in values]
        seconds = [seconds for _label, seconds in values]
        plt.plot(labels, seconds, marker="o", label=algorithm)
    plt.xlabel("Image size")
    plt.ylabel("Average time, seconds")
    plt.title("Black-and-white conversion performance")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "benchmark_results.png", dpi=160)


if __name__ == "__main__":
    generate_plot()
