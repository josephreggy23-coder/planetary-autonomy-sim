from planetary_autonomy_sim.sim import run


def test_traverse_is_reproducible():
    first = run(16, 4)
    assert first == run(16, 4)
    assert first["cells"] >= 31
    assert first["mobility_cost"] > 0
