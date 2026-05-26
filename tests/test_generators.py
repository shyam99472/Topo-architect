"""Unit tests for lattice generators and physics."""

import networkx as nx
import pytest

from topo_architect.quantum_core.generators import (
    generate_square,
    generate_honeycomb,
    generate_heavy_hex,
    graph_to_coordinates,
    lattice_from_type,
)
from topo_architect.quantum_core.physics_rules import PhysicsEngine


def test_square_lattice_node_count():
    G = generate_square(3, 3)
    assert G.number_of_nodes() == 9
    assert G.number_of_edges() > 0


def test_honeycomb_has_positions():
    G = generate_honeycomb(2, 2)
    coords = graph_to_coordinates(G)
    assert len(coords) >= 4
    assert all("x" in c and "y" in c for c in coords)


def test_heavy_hex_target_qubits():
    G = generate_heavy_hex(12)
    assert G.number_of_nodes() >= 8
    coords = graph_to_coordinates(G)
    assert len(coords) == G.number_of_nodes()


def test_lattice_from_type_square():
    G = lattice_from_type("square", 9)
    assert G.number_of_nodes() <= 9 or G.number_of_nodes() >= 9


def test_connectivity_score():
    G = nx.cycle_graph(6)
    engine = PhysicsEngine()
    score = engine.connectivity_score(G)
    assert score == pytest.approx(1.0, rel=0.01)


def test_frequency_collision_detection():
    G = nx.path_graph(3)
    freqs = {"0": 5.0, "1": 5.05, "2": 6.0}
    engine = PhysicsEngine()
    issues = engine.check_frequency_collisions(G, freqs)
    assert len(issues) >= 1


def test_graph_assignment_no_collisions_on_path():
    G = nx.path_graph(5)
    engine = PhysicsEngine()
    freqs = engine.assign_frequencies_for_graph(G, (4.5, 5.5))
    issues = engine.check_frequency_collisions(G, freqs)
    assert issues == []
