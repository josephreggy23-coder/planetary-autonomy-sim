# planetary-autonomy-sim

A deterministic autonomous-rover simulation MVP. It procedurally creates a Martian terrain grid, evaluates mobility risk, plans with Dijkstra-style cost search, then re-routes toward high-value science targets when safe.

## Quick start

```bash
python -m planetary_autonomy_sim.sim --size 32 --seed 5
pytest
```

The source layout keeps clear extension points for Open3D/PyBullet rendering, stereo perception, GTSAM SLAM, D*-Lite/MPPI control, and a Bekker–Wong terramechanics model.
