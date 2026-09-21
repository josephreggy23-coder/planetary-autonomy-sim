from planetary_autonomy_sim.report import build_report


def test_report_writes_route_and_charts(tmp_path):
    summary = build_report(tmp_path, size=12, seed=3)
    assert summary["terrain_cells"] == 144
    assert summary["route_cells"] >= 23
    assert (tmp_path / "terrain_route.svg").exists()
    assert (tmp_path / "route.csv").exists()

