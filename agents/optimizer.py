"""Agent 4: SciPy layout optimization to reduce crosstalk."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np
from scipy.optimize import minimize

from topo_architect.quantum_core.physics_rules import PhysicsEngine


class OptimizerAgent:
    def __init__(self, physics: PhysicsEngine | None = None):
        self.physics = physics or PhysicsEngine()

    def optimize_positions(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        max_iter: int = 200,
    ) -> list[dict]:
        """
        Nudge (x,y) to maximize pairwise distance while keeping edges short.
        """
        n = len(coordinates)
        if n < 2:
            return coordinates

        x0 = np.array([[c["x"], c["y"]] for c in coordinates]).flatten()
        edges = list(G.edges())
        node_ids = [c["id"] for c in coordinates]
        id_to_idx = {nid: i for i, nid in enumerate(node_ids)}

        def objective(xy):
            pts = xy.reshape(n, 2)
            # Penalize inverse-square crosstalk
            cross = 0.0
            for i in range(n):
                for j in range(i + 1, n):
                    d = np.linalg.norm(pts[i] - pts[j]) + 0.05
                    cross += 1.0 / (d * d)
            # Keep coupled qubits from drifting too far
            wire = 0.0
            for u, v in edges:
                iu = id_to_idx.get(str(u))
                iv = id_to_idx.get(str(v))
                if iu is None or iv is None:
                    continue
                d = np.linalg.norm(pts[iu] - pts[iv])
                wire += max(0, d - 2.0) ** 2
            return cross + 0.3 * wire

        res = minimize(
            objective,
            x0,
            method="L-BFGS-B",
            options={"maxiter": max_iter},
        )
        optimized = res.x.reshape(n, 2)
        out = []
        for i, c in enumerate(coordinates):
            out.append({
                **c,
                "x": round(float(optimized[i, 0]), 4),
                "y": round(float(optimized[i, 1]), 4),
            })
        return out

    def run(
        self,
        G: nx.Graph,
        coordinates: list[dict],
    ) -> dict[str, Any]:
        before = self.physics.crosstalk_estimate(coordinates)
        optimized = self.optimize_positions(G, coordinates)
        after = self.physics.crosstalk_estimate(optimized)
        return {
            "coordinates": optimized,
            "crosstalk_before": before,
            "crosstalk_after": after,
            "improvement_pct": round(
                (1 - after / before) * 100 if before > 0 else 0, 1
            ),
        }
