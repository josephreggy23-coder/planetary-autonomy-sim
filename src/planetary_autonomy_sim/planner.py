from __future__ import annotations

import heapq

from .terrain import traversability


def plan(grid: list[list[float]], start: tuple[int, int], goal: tuple[int, int]) -> tuple[list[tuple[int, int]], float]:
    height, width = len(grid), len(grid[0])
    frontier = [(0.0, start)]
    cost = {start: 0.0}
    parent = {}
    while frontier:
        total, node = heapq.heappop(frontier)
        if node == goal:
            break
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbor = (node[0] + dr, node[1] + dc)
            if not (0 <= neighbor[0] < height and 0 <= neighbor[1] < width):
                continue
            candidate = total + traversability(grid[neighbor[0]][neighbor[1]])
            if candidate < cost.get(neighbor, float("inf")):
                cost[neighbor], parent[neighbor] = candidate, node
                heapq.heappush(frontier, (candidate, neighbor))
    if goal not in cost:
        return [], float("inf")
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return list(reversed(path)), cost[goal]
