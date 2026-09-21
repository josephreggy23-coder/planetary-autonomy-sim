from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Target:
    location: tuple[int, int]
    value: float


def choose_target(targets: list[Target], travel_costs: dict[tuple[int, int], float]) -> Target | None:
    viable = [target for target in targets if target.location in travel_costs]
    return max(viable, key=lambda target: target.value / max(travel_costs[target.location], 1), default=None)
