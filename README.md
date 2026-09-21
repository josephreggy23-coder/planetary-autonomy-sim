# planetary-autonomy-sim

A deterministic autonomous-rover simulation MVP. It procedurally creates a Martian terrain grid, evaluates mobility risk, plans with Dijkstra-style cost search, then re-routes toward high-value science targets when safe.

## Quick start

```bash
python -m planetary_autonomy_sim.sim --size 32 --seed 5
pytest
```

## MVP snapshot

| Metric | Verified demo result |
| --- | ---: |
| Procedural terrain grid | 32 x 32 (1,024 cells) |
| Traverse path | 63 cells |
| Simulated traverse distance | 3.10 m at 5 cm/cell |
| Aggregate mobility cost | 187.77 |
| Reproducibility | deterministic with `--seed 5` |

These values come from `python -m planetary_autonomy_sim.sim --size 32 --seed 5`. The baseline plans a lowest-cost route across the generated terrain; it is a deliberately compact stand-in for the planned D*-Lite and MPPI stack.

## What is implemented today

| Layer | MVP implementation | Next research integration |
| --- | --- | --- |
| Terrain | seeded 0–1 roughness grid with 5 cm cells | crater, dune, and rock-field priors |
| Mobility | quadratic terrain-risk cost | slope, step, cohesion, and Bekker–Wong terms |
| Planning | deterministic Dijkstra-style lowest-cost route | incremental D*-Lite + local MPPI |
| Science | value-per-travel-cost target selector | spectral/textural anomaly detection |

The current simulation favors clear, repeatable behavior over photorealism so that future perception, SLAM, and dynamics benchmarks have a stable baseline.

The source layout keeps clear extension points for Open3D/PyBullet rendering, stereo perception, GTSAM SLAM, D*-Lite/MPPI control, and a Bekker–Wong terramechanics model.
