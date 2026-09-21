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

The source layout keeps clear extension points for Open3D/PyBullet rendering, stereo perception, GTSAM SLAM, D*-Lite/MPPI control, and a Bekker–Wong terramechanics model.
