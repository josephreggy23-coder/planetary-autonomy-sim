from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path

from .planner import plan
from .terrain import generate, traversability


def _frame(title: str, body: str, subtitle: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="640" viewBox="0 0 960 640">
<rect width="960" height="640" rx="18" fill="#0b1018"/>
<text x="50" y="48" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="25" font-weight="700">{title}</text>
<text x="50" y="75" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">{subtitle}</text>
{body}
</svg>'''


def _terrain_chart(grid: list[list[float]], path: list[tuple[int, int]]) -> str:
    size = len(grid)
    left, top, span = 150, 105, 480
    cell = span / size
    tiles = []
    for row in range(size):
        for column in range(size):
            value = grid[row][column]
            red = int(30 + 180 * value)
            green = int(210 - 125 * value)
            blue = int(140 - 80 * value)
            tiles.append(f'<rect x="{left + column * cell:.2f}" y="{top + row * cell:.2f}" width="{cell + .2:.2f}" height="{cell + .2:.2f}" fill="rgb({red},{green},{blue})"/>')
    points = " ".join(f"{left + (column + .5) * cell:.2f},{top + (row + .5) * cell:.2f}" for row, column in path)
    route = f'<polyline points="{points}" fill="none" stroke="#f8fafc" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
    legend = '''<text x="690" y="170" fill="#e2e8f0" font-family="Segoe UI, sans-serif" font-size="16" font-weight="700">Mobility risk</text>
<rect x="690" y="192" width="34" height="170" fill="url(#risk)"/>
<defs><linearGradient id="risk" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="rgb(30,210,140)"/><stop offset="1" stop-color="rgb(210,85,60)"/></linearGradient></defs>
<text x="735" y="207" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="13">high</text>
<text x="735" y="362" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="13">low</text>
<line x1="680" y1="420" x2="735" y2="420" stroke="#f8fafc" stroke-width="4"/><text x="750" y="425" fill="#e2e8f0" font-family="Segoe UI, sans-serif" font-size="13">planned route</text>'''
    return _frame("Risk-aware traverse", "\n".join(tiles) + route + legend, f"{size} × {size} seeded terrain • white path minimizes cumulative mobility cost")


def _profile_chart(grid: list[list[float]], path: list[tuple[int, int]]) -> str:
    values = [grid[row][column] for row, column in path]
    points = " ".join(f"{75 + index / max(len(values) - 1, 1) * 825:.1f},{500 - value * 350:.1f}" for index, value in enumerate(values))
    body = f'''<line x1="75" y1="500" x2="900" y2="500" stroke="#475569"/>
<line x1="75" y1="150" x2="75" y2="500" stroke="#475569"/>
<polyline points="{points}" fill="none" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<text x="488" y="555" text-anchor="middle" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">path step</text>
<text x="24" y="325" transform="rotate(-90 24 325)" text-anchor="middle" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">terrain roughness</text>'''
    return _frame("Terrain encountered along the route", body, f"{len(path)} cells • mean roughness {statistics.mean(values):.3f}")


def build_report(output_dir: Path, size: int = 64, seed: int = 5) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    grid = generate(size, seed)
    route, route_cost = plan(grid, (0, 0), (size - 1, size - 1))
    route_set = set(route)
    baseline = [(0, column) for column in range(size)] + [(row, size - 1) for row in range(1, size)]
    baseline_cost = sum(traversability(grid[row][column]) for row, column in baseline[1:])
    path_values = [grid[row][column] for row, column in route]

    with (output_dir / "terrain.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["row", "column", "roughness", "mobility_cost", "on_planned_route"])
        for row in range(size):
            for column in range(size):
                writer.writerow([row, column, f"{grid[row][column]:.6f}", f"{traversability(grid[row][column]):.6f}", (row, column) in route_set])

    with (output_dir / "route.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["step", "row", "column", "roughness", "mobility_cost"])
        for step, (row, column) in enumerate(route):
            writer.writerow([step, row, column, f"{grid[row][column]:.6f}", f"{traversability(grid[row][column]):.6f}"])

    summary = {
        "seed": seed,
        "grid_size": size,
        "terrain_cells": size * size,
        "route_cells": len(route),
        "distance_m": round((len(route) - 1) * 0.05, 2),
        "route_cost": round(route_cost, 3),
        "edge_baseline_cost": round(baseline_cost, 3),
        "cost_reduction_percent": round(100 * (baseline_cost - route_cost) / baseline_cost, 2),
        "mean_terrain_roughness": round(statistics.mean(value for row in grid for value in row), 4),
        "mean_route_roughness": round(statistics.mean(path_values), 4),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_dir / "terrain_route.svg").write_text(_terrain_chart(grid, route), encoding="utf-8")
    (output_dir / "route_roughness.svg").write_text(_profile_chart(grid, route), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate rover benchmark data and charts.")
    parser.add_argument("--output", type=Path, default=Path("results/demo"))
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--seed", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(build_report(args.output, args.size, args.seed), indent=2))


if __name__ == "__main__":
    main()
