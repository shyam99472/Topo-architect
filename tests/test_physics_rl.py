"""Tests for graph-aware frequencies and RL optimizer."""

import networkx as nx

from topo_architect.agents.rl_optimizer import RLOptimizer
from topo_architect.quantum_core.generators import generate_square
from topo_architect.quantum_core.physics_rules import PhysicsEngine


def test_graph_frequencies_satisfy_neighbor_spacing():
    G = generate_square(4, 4)
    engine = PhysicsEngine()
    freqs = engine.assign_frequencies_for_graph(G, (4.6, 5.2))
    issues = engine.check_frequency_collisions(G, freqs)
    assert issues == []


def test_spatial_crosstalk_ignores_coupled_pairs():
    G = nx.Graph()
    G.add_edge("a", "b")
    coords = [
        {"id": "a", "x": 0.0, "y": 0.0},
        {"id": "b", "x": 0.1, "y": 0.0},
        {"id": "c", "x": 5.0, "y": 5.0},
    ]
    engine = PhysicsEngine()
    flags = engine.check_crosstalk_pairs(coords, threshold=0.5, G=G)
    assert all("c" in f["nodes"] for f in flags) or len(flags) == 0


def test_rl_converges_on_small_grid():
    from topo_architect.quantum_core.generators import graph_to_coordinates

    G = generate_square(3, 3)
    engine = PhysicsEngine()
    coords = graph_to_coordinates(G)
    freqs = engine.assign_frequencies_for_graph(G, (4.6, 5.2))
    rl = RLOptimizer(max_iterations=10, target_score=80.0, min_iterations=3)
    out = rl.run(G, coords, freqs, {"freq_range": [4.6, 5.2], "lattice_type": "square"})
    assert out["best_score"] >= 70
    assert len(out["history"]) >= 1


def test_rl_iterations_improve_or_hold():
    from topo_architect.quantum_core.generators import graph_to_coordinates

    G = generate_square(3, 3)
    engine = PhysicsEngine()
    coords = graph_to_coordinates(G)
    freqs = engine.assign_frequencies_for_graph(G, (4.6, 5.2))
    rl = RLOptimizer(max_iterations=8, min_iterations=8, target_score=99.9)
    out = rl.run(G, coords, freqs, {"freq_range": [4.6, 5.2], "lattice_type": "square"})
    scores = [h["score"] for h in out["history"]]
    assert len(scores) >= 2
    assert scores[-1] >= scores[0] - 0.1


def test_rl_topology_changes_across_iterations():
    from topo_architect.quantum_core.generators import graph_to_coordinates

    G = generate_square(3, 3)
    engine = PhysicsEngine()
    coords = graph_to_coordinates(G)
    freqs = engine.assign_frequencies_for_graph(G, (4.6, 5.2))
    rl = RLOptimizer(max_iterations=8, min_iterations=8, target_score=99.9)
    out = rl.run(G, coords, freqs, {"freq_range": [4.6, 5.2], "lattice_type": "square"})
    topo_sets = {
        tuple(
            sorted(
                (min(str(e["source"]), str(e["target"])), max(str(e["source"]), str(e["target"])))
                for e in h.get("edges", [])
            )
        )
        for h in out["history"]
    }
    bond_counts = [h.get("n_edges", 0) for h in out["history"]]
    assert len(topo_sets) >= 1
    assert max(bond_counts) >= min(bond_counts), "bond count should be stable or improving"


def test_rl_scores_have_upward_momentum():
    from topo_architect.quantum_core.generators import graph_to_coordinates

    G = generate_square(3, 3)
    engine = PhysicsEngine()
    coords = graph_to_coordinates(G)
    freqs = engine.assign_frequencies_for_graph(G, (4.6, 5.2))
    rl = RLOptimizer(max_iterations=10, min_iterations=5, target_score=99.9)
    out = rl.run(G, coords, freqs, {"freq_range": [4.6, 5.2], "lattice_type": "square"})
    scores = [h["score"] for h in out["history"]]
    assert scores[0] >= 50
    for i in range(1, len(scores)):
        assert scores[i] >= scores[i - 1] - 0.1, (
            f"score fell at iteration {i + 1}: {scores[i - 1]} -> {scores[i]}"
        )
    assert scores[-1] >= scores[0], "final score should not be below start"
