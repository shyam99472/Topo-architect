"""Agent 3: Physics / crosstalk validation."""

from __future__ import annotations

from typing import Any

import networkx as nx

from topo_architect.quantum_core.physics_rules import PhysicsEngine


class ValidatorAgent:
    def __init__(
        self,
        distance_threshold: float = 0.5,
        physics: PhysicsEngine | None = None,
    ):
        self.distance_threshold = distance_threshold
        self.physics = physics or PhysicsEngine()

    def validate(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        frequencies: dict[str, float],
        lattice_type: str = "heavy_hex",
    ) -> dict[str, Any]:
        metrics = self.physics.full_metrics(
            G, coordinates, frequencies, lattice_type=lattice_type
        )
        errors = []
        warnings = []

        for issue in metrics.get("freq_issues", []):
            errors.append(issue["message"])

        for issue in metrics.get("spatial_issues", []):
            errors.append(issue["message"])

        if not metrics.get("connectivity_ok", True):
            warnings.append(
                f"Connectivity C={metrics['connectivity_score']:.2f} "
                f"deviates from target ~{metrics['connectivity_target']}"
            )

        density = metrics.get("layout_density", 0)
        if density > 50:
            warnings.append(f"High layout density ({density}) may increase crosstalk")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "metrics": metrics,
        }
