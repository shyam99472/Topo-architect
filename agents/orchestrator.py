"""Multi-agent orchestrator: Analyst → Designer → Validator → RL Optimizer → Reporter."""

from __future__ import annotations

import copy
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import networkx as nx

from topo_architect.agents.analyst import AnalystAgent
from topo_architect.agents.designer import DesignerAgent
from topo_architect.agents.optimizer import OptimizerAgent
from topo_architect.agents.reporter import ReporterAgent
from topo_architect.agents.rl_optimizer import RLOptimizer
from topo_architect.agents.validator import ValidatorAgent
from topo_architect.quantum_core.physics_rules import PhysicsEngine


def _graph_to_serializable(G: nx.Graph) -> dict:
    return {
        "nodes": [str(n) for n in G.nodes()],
        "edges": [{"source": str(u), "target": str(v)} for u, v in G.edges()],
    }


class AgentOrchestrator:
    def __init__(
        self,
        max_rl_iterations: int = 15,
        min_rl_iterations: int | None = None,
        target_rl_score: float = 92.0,
    ):
        self.analyst = AnalystAgent()
        self.designer = DesignerAgent()
        self.validator = ValidatorAgent()
        self.layout_optimizer = OptimizerAgent()
        min_iters = min_rl_iterations or max(5, max_rl_iterations // 2)
        self.rl_optimizer = RLOptimizer(
            max_iterations=max_rl_iterations,
            min_iterations=min_iters,
            target_score=target_rl_score,
        )
        self.reporter = ReporterAgent()
        self.physics = PhysicsEngine()
        self._db_path = Path(__file__).resolve().parents[1] / "database" / "schema.json"

    def run(
        self,
        user_prompt: str,
        optimize: bool = True,
        max_rl_iterations: int | None = None,
    ) -> dict[str, Any]:
        design_id = f"design_{uuid.uuid4().hex[:8]}"

        if max_rl_iterations is not None:
            self.rl_optimizer.max_iterations = max_rl_iterations

        config = self.analyst.parse(user_prompt)
        design = self.designer.design(config)
        G: nx.Graph = design["graph"]
        G_initial = G.copy()
        coordinates = design["coordinates"]
        edges = design["edges"]

        freq_range = tuple(config.get("freq_range", [4.5, 5.5]))
        frequencies = self.physics.assign_frequencies_for_graph(G, freq_range)
        self.physics.sync_coordinate_frequencies(coordinates, frequencies)

        validation_pre = self.validator.validate(
            G_initial, coordinates, frequencies, lattice_type=config.get("lattice_type", "")
        )

        optimization: dict[str, Any] = {
            "mode": "none",
            "coordinates": coordinates,
            "crosstalk_before": self.physics.crosstalk_estimate(coordinates),
            "crosstalk_after": self.physics.crosstalk_estimate(coordinates),
            "improvement_pct": 0,
        }
        rl_result: dict[str, Any] | None = None

        if optimize and len(coordinates) >= 2:
            rl_result = self.rl_optimizer.run(G, coordinates, frequencies, config)
            coordinates = rl_result["coordinates"]
            frequencies = rl_result["frequencies"]
            if rl_result.get("edges"):
                edges = rl_result["edges"]
                G = nx.Graph()
                for c in coordinates:
                    G.add_node(str(c["id"]))
                for e in edges:
                    G.add_edge(str(e["source"]), str(e["target"]))
            optimization = {
                "mode": "rl",
                "coordinates": coordinates,
                "crosstalk_before": validation_pre.get("metrics", {}).get(
                    "crosstalk_estimate", 0
                ),
                "crosstalk_after": self.physics.crosstalk_estimate(coordinates),
                "improvement_pct": round(
                    (
                        1
                        - self.physics.crosstalk_estimate(coordinates)
                        / max(
                            0.001,
                            validation_pre.get("metrics", {}).get("crosstalk_estimate", 1),
                        )
                    )
                    * 100,
                    1,
                ),
                "rl_history": rl_result.get("history", []),
                "rl_iterations": rl_result.get("history", []),
                "ranking": sorted(
                    [
                        {"iteration": h["iteration"], "score": h["score"], "valid": h["valid"]}
                        for h in rl_result.get("history", [])
                    ],
                    key=lambda x: x["score"],
                    reverse=True,
                ),
                "best_iteration": rl_result.get("best_iteration"),
                "best_score": rl_result.get("best_score"),
                "converged": rl_result.get("converged"),
                "iterations_run": rl_result.get("iterations_run"),
            }

        validation = self.validator.validate(
            G, coordinates, frequencies, lattice_type=config.get("lattice_type", "")
        )

        report_md = self.reporter.build_report(
            config, design, validation, optimization, user_prompt=user_prompt
        )
        export_paths = self.reporter.export_artifacts(
            design_id,
            config,
            coordinates,
            edges,
            report_md,
            frequencies,
        )

        result = {
            "design_id": design_id,
            "config": config,
            "coordinates": coordinates,
            "edges": edges,
            "frequencies": frequencies,
            "graph": _graph_to_serializable(G),
            "validation": validation,
            "validation_pre": validation_pre,
            "optimization": optimization,
            "rl": rl_result,
            "report_markdown": report_md,
            "export_paths": export_paths,
            "designer_notes": self.designer.suggest_layout_tweaks(
                config, validation.get("metrics", {})
            ),
        }
        self._save_history(result)
        return result

    def run_streaming(
        self,
        user_prompt: str,
        optimize: bool = True,
        max_rl_iterations: int | None = None,
        min_rl_iterations: int | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Yield progress events; final event contains full result."""
        if max_rl_iterations is not None:
            self.rl_optimizer.max_iterations = max_rl_iterations
        if min_rl_iterations is not None:
            self.rl_optimizer.min_iterations = min_rl_iterations
        elif max_rl_iterations is not None:
            self.rl_optimizer.min_iterations = max(3, max_rl_iterations // 2)

        design_id = f"design_{uuid.uuid4().hex[:8]}"

        yield {"type": "status", "message": "Analyst agent: parsing prompt…"}
        config = self.analyst.parse(user_prompt)
        yield {"type": "status", "message": "Designer agent: building topology…"}
        design = self.designer.design(config)
        G: nx.Graph = design["graph"]
        G_initial = G.copy()
        coordinates = design["coordinates"]
        edges = design["edges"]

        freq_range = tuple(config.get("freq_range", [4.5, 5.5]))
        frequencies = self.physics.assign_frequencies_for_graph(G, freq_range)
        self.physics.sync_coordinate_frequencies(coordinates, frequencies)

        base = {
            "design_id": design_id,
            "config": config,
            "edges": edges,
            "graph": _graph_to_serializable(G),
        }

        yield {
            "type": "initial_design",
            **base,
            "coordinates": coordinates,
            "frequencies": frequencies,
        }

        rl_history: list[dict[str, Any]] = []
        best_coords = copy.deepcopy(coordinates)
        best_freqs = dict(frequencies)
        best_edges = copy.deepcopy(edges)
        rl_meta: dict[str, Any] = {}

        if optimize and len(coordinates) >= 2:
            yield {"type": "status", "message": "RL optimizer: starting iterations…"}
            for event in self.rl_optimizer.run_iterative(
                G, coordinates, frequencies, config
            ):
                if event["type"] == "rl_iteration":
                    rl_history.append({
                        "iteration": event["iteration"],
                        "score": event["score"],
                        "valid": event["valid"],
                        "is_best": event["is_best"],
                        "errors": event["errors"],
                        "warnings": event["warnings"],
                        "metrics": event["metrics"],
                        "coordinates": event["coordinates"],
                        "frequencies": event["frequencies"],
                        "edges": event.get("edges", []),
                        "n_edges": event.get("n_edges", 0),
                        "layout_fingerprint": event.get("layout_fingerprint"),
                        "topology_fingerprint": event.get("topology_fingerprint"),
                    })
                    if event["is_best"]:
                        best_coords = copy.deepcopy(event["coordinates"])
                        best_freqs = dict(event["frequencies"])
                        best_edges = copy.deepcopy(event.get("edges", best_edges))
                    yield {**base, **event}
                elif event["type"] == "rl_complete":
                    rl_meta = event
                    best_it = event.get("best_iteration")
                    for h in rl_history:
                        h["is_best"] = h["iteration"] == best_it
                    winner = next(
                        (h for h in rl_history if h["iteration"] == best_it),
                        rl_history[-1] if rl_history else None,
                    )
                    if winner:
                        best_coords = copy.deepcopy(winner["coordinates"])
                        best_freqs = dict(winner["frequencies"])
                        best_edges = copy.deepcopy(winner.get("edges", best_edges))
                    yield {**base, **event}

        coordinates = best_coords
        frequencies = best_freqs
        edges = best_edges
        G = nx.Graph()
        for c in coordinates:
            G.add_node(str(c["id"]))
        for e in edges:
            G.add_edge(str(e["source"]), str(e["target"]))

        validation_pre = self.validator.validate(
            G_initial,
            design["coordinates"],
            self.physics.assign_frequencies_for_graph(G_initial, freq_range),
            lattice_type=config.get("lattice_type", ""),
        )
        validation = self.validator.validate(
            G, coordinates, frequencies, lattice_type=config.get("lattice_type", "")
        )

        optimization = {
            "mode": "rl" if optimize else "none",
            "best_iteration": rl_meta.get("best_iteration"),
            "best_score": rl_meta.get("best_score"),
            "converged": rl_meta.get("converged", False),
            "iterations_run": rl_meta.get("iterations_run", len(rl_history)),
            "rl_history": rl_history,
            "rl_iterations": rl_history,
            "ranking": rl_meta.get("ranking", []),
            "min_iterations": rl_meta.get("min_iterations"),
        }

        yield {"type": "status", "message": "Reporter agent: generating exports…"}
        report_md = self.reporter.build_report(
            config,
            design,
            validation,
            optimization,
            user_prompt=user_prompt,
        )
        export_paths = self.reporter.export_artifacts(
            design_id, config, coordinates, edges, report_md, frequencies
        )

        result = {
            **base,
            "coordinates": coordinates,
            "edges": edges,
            "frequencies": frequencies,
            "graph": _graph_to_serializable(G),
            "validation": validation,
            "validation_pre": validation_pre,
            "optimization": optimization,
            "rl": rl_meta,
            "report_markdown": report_md,
            "export_paths": export_paths,
            "designer_notes": self.designer.suggest_layout_tweaks(
                config, validation.get("metrics", {})
            ),
            "best_iteration_snapshot": next(
                (h for h in rl_history if h["iteration"] == rl_meta.get("best_iteration")),
                rl_history[-1] if rl_history else None,
            ),
        }
        self._save_history(result)
        yield {"type": "final", "result": result}

    def _save_history(self, result: dict) -> None:
        try:
            data = json.loads(self._db_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"version": "1.0", "designs": []}

        entry = {
            "design_id": result["design_id"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "config": result["config"],
            "valid": result["validation"].get("valid"),
            "rl_score": (result.get("optimization") or {}).get("best_score"),
            "metrics": result["validation"].get("metrics"),
        }
        data.setdefault("designs", []).append(entry)
        self._db_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def run_pipeline(
    user_prompt: str,
    optimize: bool = True,
    max_rl_iterations: int = 15,
) -> dict[str, Any]:
    return AgentOrchestrator(max_rl_iterations=max_rl_iterations).run(
        user_prompt, optimize=optimize
    )
