"""NetworkX lattice generators and coordinate export for qubit layouts."""

from __future__ import annotations

import math
from typing import Literal

import networkx as nx

LatticeType = Literal["square", "honeycomb", "heavy_hex"]


def _dims_for_qubits(n_qubits: int, lattice_type: LatticeType) -> tuple[int, int]:
    """Estimate grid dimensions to reach at least n_qubits nodes."""
    if lattice_type == "square":
        side = max(2, int(math.ceil(math.sqrt(n_qubits))))
        return side, side
    # Hex lattices need more rows/cols for same qubit count
    side = max(2, int(math.ceil(math.sqrt(n_qubits * 0.75))))
    return side, side


def generate_square(rows: int, cols: int) -> nx.Graph:
    """Standard i,j grid lattice."""
    G = nx.grid_2d_graph(rows, cols)
    return _relabel_grid(G)


def generate_honeycomb(rows: int, cols: int) -> nx.Graph:
    """Classic hexagonal tiling via NetworkX hexagonal lattice."""
    G = nx.hexagonal_lattice_graph(rows, cols, with_positions=True, periodic=False)
    return _relabel_positions(G)


def generate_heavy_hex(n_qubits: int) -> nx.Graph:
    """
    IBM-style heavy-hex: hexagonal lattice plus bridge qubits on edges.
    """
    rows, cols = _dims_for_qubits(n_qubits, "heavy_hex")
    base = nx.hexagonal_lattice_graph(rows, cols, with_positions=True, periodic=False)
    G = _relabel_positions(base)

    bridge_nodes = []
    for u, v in list(G.edges()):
        pos_u = G.nodes[u].get("pos", (0.0, 0.0))
        pos_v = G.nodes[v].get("pos", (0.0, 0.0))
        mid = ((pos_u[0] + pos_v[0]) / 2, (pos_u[1] + pos_v[1]) / 2)
        bridge_id = f"b_{u}_{v}"
        if bridge_id in G:
            continue
        G.add_node(bridge_id, pos=mid, role="bridge")
        G.add_edge(u, bridge_id)
        G.add_edge(bridge_id, v)
        bridge_nodes.append(bridge_id)

    # Trim or pad to target qubit count
    nodes = list(G.nodes())
    if len(nodes) > n_qubits:
        # Prefer keeping data qubits over bridges when trimming
        data_nodes = [n for n in nodes if G.nodes[n].get("role") != "bridge"]
        bridge_only = [n for n in nodes if G.nodes[n].get("role") == "bridge"]
        keep = data_nodes[: max(1, n_qubits - min(len(bridge_only), n_qubits // 4))]
        remaining = n_qubits - len(keep)
        keep += bridge_only[:remaining]
        remove = [n for n in nodes if n not in keep]
        G.remove_nodes_from(remove)
    elif len(nodes) < n_qubits:
        for i in range(n_qubits - len(nodes)):
            nid = f"extra_{i}"
            G.add_node(nid, pos=(i * 1.2, 0.0), role="pad")

    return G


def lattice_from_type(
    lattice_type: str,
    n_qubits: int,
    dimensions: tuple[int, int] | None = None,
) -> nx.Graph:
    """Build graph from lattice type string."""
    lt = lattice_type.lower().replace("-", "_").replace(" ", "_")
    if dimensions:
        rows, cols = dimensions
    else:
        rows, cols = _dims_for_qubits(n_qubits, lt if lt in ("square", "honeycomb") else "heavy_hex")

    if lt in ("square", "grid"):
        G = generate_square(rows, cols)
    elif lt in ("honeycomb", "hex", "hexagonal"):
        G = generate_honeycomb(rows, cols)
    elif lt in ("heavy_hex", "heavyhex", "ibm", "heavy_hexagonal"):
        G = generate_heavy_hex(n_qubits)
    else:
        G = generate_heavy_hex(n_qubits)

    # Trim square/honeycomb to n_qubits
    nodes = list(G.nodes())
    if lt not in ("heavy_hex", "heavyhex", "ibm", "heavy_hexagonal") and len(nodes) > n_qubits:
        G = G.subgraph(nodes[:n_qubits]).copy()

    return G


def graph_to_coordinates(G: nx.Graph, spacing: float = 1.0) -> list[dict]:
    """
    Convert graph nodes to (x, y) qubit coordinates.
    Uses stored 'pos' or spring layout as fallback.
    """
    if not G.nodes():
        return []

    has_pos = all("pos" in G.nodes[n] for n in G.nodes())
    if not has_pos:
        pos = nx.spring_layout(G, seed=42, scale=spacing)
        for n, p in pos.items():
            G.nodes[n]["pos"] = (float(p[0]), float(p[1]))

    coords = []
    for i, node in enumerate(G.nodes()):
        px, py = G.nodes[node].get("pos", (0.0, 0.0))
        coords.append({
            "id": str(node),
            "index": i,
            "x": round(float(px) * spacing, 4),
            "y": round(float(py) * spacing, 4),
            "role": G.nodes[node].get("role", "data"),
            "degree": G.degree(node),
        })
    return coords


def _relabel_grid(G: nx.Graph) -> nx.Graph:
    """Relabel grid_2d nodes to q0, q1, ... with positions."""
    H = nx.Graph()
    spacing = 1.0
    for i, (r, c) in enumerate(G.nodes()):
        nid = f"q{i}"
        H.add_node(nid, pos=(c * spacing, r * spacing), role="data")
    for (r1, c1), (r2, c2) in G.edges():
        i1 = list(G.nodes()).index((r1, c1))
        i2 = list(G.nodes()).index((r2, c2))
        H.add_edge(f"q{i1}", f"q{i2}")
    return H


def _relabel_positions(G: nx.Graph) -> nx.Graph:
    """Relabel hex lattice nodes preserving positions."""
    H = nx.Graph()
    node_map = {}
    for i, n in enumerate(G.nodes()):
        nid = f"q{i}"
        node_map[n] = nid
        pos = G.nodes[n].get("pos", (0.0, 0.0))
        H.add_node(nid, pos=pos, role="data")
    for u, v in G.edges():
        H.add_edge(node_map[u], node_map[v])
    return H
