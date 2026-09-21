from __future__ import annotations

import random


def generate(size: int, seed: int = 0) -> list[list[float]]:
    """Generate a reproducible slope/roughness proxy in [0, 1]."""
    rng = random.Random(seed)
    grid = [[rng.random() for _ in range(size)] for _ in range(size)]
    grid[0][0] = 0.0
    grid[-1][-1] = 0.0
    return grid


def traversability(cell: float) -> float:
    """Return a travel cost; high roughness becomes prohibitively costly."""
    return 1.0 + 20.0 * cell * cell
