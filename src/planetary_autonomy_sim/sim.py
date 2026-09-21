from __future__ import annotations

import argparse

from .planner import plan
from .terrain import generate


def run(size: int, seed: int) -> dict:
    grid = generate(size, seed)
    path, cost = plan(grid, (0, 0), (size - 1, size - 1))
    return {"distance_m": (len(path) - 1) * 0.05, "cells": len(path), "mobility_cost": round(cost, 2)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a simulated autonomous rover traverse.")
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    print(run(args.size, args.seed))


if __name__ == "__main__":
    main()
