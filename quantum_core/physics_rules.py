"""Physics simulation: frequency crowding, connectivity, crosstalk."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np


FREQ_COLLISION_MHZ = 200.0
MIN_NEIGHBOR_SPACING_GHZ = FREQ_COLLISION_MHZ / 1000.0  # 0.2 GHz
TARGET_CONNECTIVITY_HEAVY_HEX = 3.0


class PhysicsEngine:
    """Rule-based physics checks for superconducting qubit layouts."""

    def __init__(self, freq_collision_mhz: float = FREQ_COLLISION_MHZ):
        self.freq_collision_mhz = freq_collision_mhz
        self.freq_collision_ghz = freq_collision_mhz / 1000.0

    def assign_frequencies_for_graph(
        self,
        G: nx.Graph,
        freq_range: tuple[float, float] = (4.5, 5.5),
        min_spacing_ghz: float | None = None,
    ) -> dict[str, float]:
        """
        Assign frequencies so coupled neighbors are at least min_spacing apart.
        Greedy assignment ordered by node degree (highest first).
        """
        min_spacing = min_spacing_ghz or self.freq_collision_ghz
        low, high = float(freq_range[0]), float(freq_range[1])
        if low > high:
            low, high = high, low

        nodes = list(G.nodes())
        if not nodes:
            return {}

        if len(nodes) == 1:
            return {str(nodes[0]): round((low + high) / 2, 4)}

        n_candidates = max(32, len(nodes) * 4)
        candidates = np.linspace(low, high, n_candidates)
        order = sorted(nodes, key=lambda n: G.degree(n), reverse=True)
        freqs: dict[str, float] = {}

        for node in order:
            neighbors = [n for n in G.neighbors(node) if n in freqs]
            neighbor_vals = [freqs[n] for n in neighbors]

            best_f = low
            best_margin = -1.0

            for f in candidates:
                if not neighbor_vals:
                    best_f = float(f)
                    best_margin = min_spacing
                    break
                margin = min(abs(float(f) - fn) for fn in neighbor_vals)
                if margin >= min_spacing and margin > best_margin:
                    best_f = float(f)
                    best_margin = margin

            if best_margin < min_spacing:
                for f in candidates:
                    if not neighbor_vals:
                        best_f = float(f)
                        best_margin = min_spacing
                        break
                    margin = min(abs(float(f) - fn) for fn in neighbor_vals)
                    if margin > best_margin:
                        best_f = float(f)
                        best_margin = margin

            freqs[node] = round(best_f, 4)

        return {str(k): v for k, v in freqs.items()}

    def assign_frequencies(
        self,
        n_qubits: int,
        freq_range: tuple[float, float] = (4.5, 5.5),
        spacing_ghz: float | None = None,
    ) -> list[float]:
        """Legacy list assignment (index order) — prefer assign_frequencies_for_graph."""
        spacing = spacing_ghz or self.freq_collision_ghz
        low, high = freq_range
        if n_qubits <= 1:
            return [round((low + high) / 2, 4)]
        freqs = np.linspace(low, high, n_qubits)
        for i in range(1, len(freqs)):
            if freqs[i] - freqs[i - 1] < spacing:
                freqs[i] = freqs[i - 1] + spacing
        return [round(float(f), 4) for f in freqs[:n_qubits]]

    def sync_coordinate_frequencies(
        self,
        coordinates: list[dict],
        frequencies: dict[str, float],
    ) -> None:
        for c in coordinates:
            c["frequency_ghz"] = frequencies.get(str(c["id"]), 0.0)

    def check_frequency_collisions(
        self,
        G: nx.Graph,
        frequencies: dict[str, float],
    ) -> list[dict[str, Any]]:
        """Flag coupled pairs with Δf below minimum (frequency crowding)."""
        issues = []
        checked: set[tuple[str, str]] = set()
        min_mhz = self.freq_collision_mhz

        for u, v in G.edges():
            key = tuple(sorted([str(u), str(v)]))
            if key in checked:
                continue
            checked.add(key)
            fu = frequencies.get(str(u))
            fv = frequencies.get(str(v))
            if fu is None or fv is None:
                continue
            delta_ghz = abs(fu - fv)
            delta_mhz = delta_ghz * 1000.0
            if delta_ghz < self.freq_collision_ghz:
                issues.append({
                    "type": "frequency_collision",
                    "nodes": [str(u), str(v)],
                    "delta_mhz": round(delta_mhz, 1),
                    "message": (
                        f"Frequency crowding: {u}↔{v} Δf={delta_mhz:.1f} MHz "
                        f"(need ≥ {min_mhz:.0f} MHz between coupled qubits)"
                    ),
                })
        return issues

    def connectivity_score(self, G: nx.Graph) -> float:
        """C = E / V (edges per vertex)."""
        v = G.number_of_nodes()
        e = G.number_of_edges()
        if v == 0:
            return 0.0
        return round(e / v, 3)

    def layout_density(self, coordinates: list[dict]) -> float:
        if len(coordinates) < 2:
            return 0.0
        xs = [c["x"] for c in coordinates]
        ys = [c["y"] for c in coordinates]
        area = max(0.01, (max(xs) - min(xs)) * (max(ys) - min(ys)))
        return round(len(coordinates) / area, 3)

    def crosstalk_estimate(self, coordinates: list[dict]) -> float:
        n = len(coordinates)
        if n < 2:
            return 0.0
        total = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                dx = coordinates[i]["x"] - coordinates[j]["x"]
                dy = coordinates[i]["y"] - coordinates[j]["y"]
                d = max(0.05, (dx * dx + dy * dy) ** 0.5)
                total += 1.0 / (d * d)
        return round(total, 4)

    def _edge_set(self, G: nx.Graph | None) -> set[tuple[str, str]]:
        if G is None:
            return set()
        return {tuple(sorted([str(u), str(v)])) for u, v in G.edges()}

    def check_crosstalk_pairs(
        self,
        coordinates: list[dict],
        threshold: float = 0.45,
        G: nx.Graph | None = None,
    ) -> list[dict[str, Any]]:
        """
        Flag *non-coupled* qubit pairs that are too close in space.
        Coupled neighbors are allowed to be near each other.
        """
        flags = []
        coupled = self._edge_set(G)
        n = len(coordinates)
        for i in range(n):
            for j in range(i + 1, n):
                id1, id2 = str(coordinates[i]["id"]), str(coordinates[j]["id"])
                if tuple(sorted([id1, id2])) in coupled:
                    continue
                dx = coordinates[i]["x"] - coordinates[j]["x"]
                dy = coordinates[i]["y"] - coordinates[j]["y"]
                d = (dx * dx + dy * dy) ** 0.5
                if d < threshold:
                    flags.append({
                        "type": "crosstalk",
                        "nodes": [id1, id2],
                        "distance": round(d, 4),
                        "message": (
                            f"Spatial crosstalk: {id1}↔{id2} dist={d:.3f} "
                            f"(non-coupled, need ≥ {threshold})"
                        ),
                    })
        return flags

    def full_metrics(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        frequencies: dict[str, float],
        lattice_type: str = "heavy_hex",
    ) -> dict[str, Any]:
        conn = self.connectivity_score(G)
        target = TARGET_CONNECTIVITY_HEAVY_HEX
        freq_issues = self.check_frequency_collisions(G, frequencies)
        spatial_flags = self.check_crosstalk_pairs(coordinates, G=G)
        return {
            "connectivity_score": conn,
            "connectivity_target": target,
            "connectivity_ok": abs(conn - target) < 1.2 if "heavy" in lattice_type.lower() else True,
            "layout_density": self.layout_density(coordinates),
            "crosstalk_estimate": self.crosstalk_estimate(coordinates),
            "frequency_collisions": len(freq_issues),
            "spatial_crosstalk_flags": len(spatial_flags),
            "freq_issues": freq_issues,
            "spatial_issues": spatial_flags,
        }
