"""Benchmark slow and optimized black-and-white conversion implementations."""

from __future__ import annotations

import csv
import time
from collections.abc import Callable
from pathlib import Path

import numpy as np
from PIL import Image

from bw_converter.algorithms import ALGORITHMS, convert_image

RESULTS_PATH = Path("benchmark_results.csv")
SIZES = [(256, 256), (512, 512), (1024, 1024)]
REPEATS = 3


def make_image(size: tuple[int, int]) -> Image.Image:
    """Generate a deterministic RGB image for benchmarking."""
    rng = np.random.default_rng(seed=size[0] * size[1])
    data = rng.integers(0, 256, size=(size[1], size[0], 3), dtype=np.uint8)
    return Image.fromarray(data, mode="RGB")


def slow_luminosity(image: Image.Image) -> Image.Image:
    """Slow baseline implementation using Python pixel loops."""
    rgb = image.convert("RGB")
    result = Image.new("L", rgb.size)
    source = rgb.load()
    target = result.load()
    width, height = rgb.size
    for y_pos in range(height):
        for x_pos in range(width):
            red, green, blue = source[x_pos, y_pos]
            target[x_pos, y_pos] = int(0.299 * red + 0.587 * green + 0.114 * blue)
    return result


def measure(
    function: Callable[[Image.Image], Image.Image], image: Image.Image
) -> float:
    """Measure average execution time for a conversion function."""
    times: list[float] = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        function(image)
        times.append(time.perf_counter() - start)
    return sum(times) / len(times)


def run_benchmark() -> None:
    """Run benchmarks and save results to CSV."""
    rows: list[dict[str, str]] = []
    for size in SIZES:
        image = make_image(size)
        slow_time = measure(slow_luminosity, image)
        rows.append(
            {
                "algorithm": "luminosity_slow_loop",
                "width": str(size[0]),
                "height": str(size[1]),
                "seconds": f"{slow_time:.6f}",
            },
        )
        for algorithm in ALGORITHMS:
            optimized_time = measure(
                lambda img, name=algorithm: convert_image(
                    img,
                    name,
                    threshold_value=128,
                ),
                image,
            )
            rows.append(
                {
                    "algorithm": algorithm,
                    "width": str(size[0]),
                    "height": str(size[1]),
                    "seconds": f"{optimized_time:.6f}",
                },
            )

    with RESULTS_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["algorithm", "width", "height", "seconds"]
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    run_benchmark()
