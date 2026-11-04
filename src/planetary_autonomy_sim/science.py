from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Target:
    """A science site on the terrain grid and its estimated scientific value."""

    location: tuple[int, int]
    value: float


def choose_target(targets: list[Target], travel_costs: dict[tuple[int, int], float]) -> Target | None:
    """Return the reachable target with the best value per unit travel cost, or None."""
    viable = [target for target in targets if target.location in travel_costs]
    return max(viable, key=lambda target: target.value / max(travel_costs[target.location], 1), default=None)
