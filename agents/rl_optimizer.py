"""RL-driven chip design loop — explore layouts/frequencies, validate, keep best."""

from __future__ import annotations

import copy
import hashlib
import math
import random
from typing import Any, Iterator

import networkx as nx
import numpy as np

from topo_architect.agents.optimizer import OptimizerAgent
from topo_architect.agents.validator import ValidatorAgent
from topo_architect.quantum_core.physics_rules import PhysicsEngine


def _edges_from_graph(G: nx.Graph) -> list[dict[str, str]]:
    return [{"source": str(u), "target": str(v)} for u, v in G.edges()]


def _topology_fingerprint(edges: list[dict]) -> str:
    pairs = sorted(
        f"{min(str(e['source']), str(e['target']))}-"
        f"{max(str(e['source']), str(e['target']))}"
        for e in edges
    )
    return hashlib.md5(",".join(pairs).encode()).hexdigest()[:10]


def _layout_fingerprint(
    coordinates: list[dict],
    frequencies: dict[str, float],
    edges: list[dict] | None = None,
) -> str:
    parts = [_topology_fingerprint(edges or [])]
    for c in sorted(coordinates, key=lambda x: str(x["id"])):
        parts.append(f"{c['id']}:{round(float(c['x']), 3)},{round(float(c['y']), 3)}")
    for k in sorted(frequencies.keys()):
        parts.append(f"{k}={round(float(frequencies[k]), 4)}")
    return hashlib.md5("|".join(parts).encode()).hexdigest()[:10]


class RLOptimizer:
    """
    Elitist hill-climb: each iteration builds on the best design so far.
    Scores should rise (or hold) — never random walk downward.
    """

    MAX_DEGREE = 4
    SCORE_EPS = 0.05  # tie tolerance when comparing candidates

    def __init__(
        self,
        max_iterations: int = 15,
        min_iterations: int = 5,
        target_score: float = 92.0,
        physics: PhysicsEngine | None = None,
        validator: ValidatorAgent | None = None,
        layout_optimizer: OptimizerAgent | None = None,
    ):
        self.max_iterations = max_iterations
        self.min_iterations = min_iterations
        self.target_score = target_score
        self.physics = physics or PhysicsEngine()
        self.validator = validator or ValidatorAgent(physics=self.physics)
        self.layout_optimizer = layout_optimizer or OptimizerAgent(physics=self.physics)

    def compute_score(
        self,
        validation: dict[str, Any],
        metrics: dict[str, Any],
    ) -> float:
        score = 100.0
        score -= len(validation.get("errors", [])) * 14.0
        score -= len(validation.get("warnings", [])) * 2.5
        score -= metrics.get("crosstalk_estimate", 0) * 0.35
        score -= metrics.get("frequency_collisions", 0) * 10.0
        score -= metrics.get("spatial_crosstalk_flags", 0) * 8.0
        score -= metrics.get("layout_density", 0) * 0.08
        if validation.get("valid"):
            score += 8.0
        if metrics.get("connectivity_ok"):
            score += 3.0
        return round(max(5.0, min(99.5, score)), 1)

    @staticmethod
    def _layout_span(coordinates: list[dict]) -> float:
        if not coordinates:
            return 1.0
        xs = [float(c["x"]) for c in coordinates]
        ys = [float(c["y"]) for c in coordinates]
        return max(max(xs) - min(xs), max(ys) - min(ys), 0.5)

    def _mutate_positions(
        self,
        coordinates: list[dict],
        learning_rate: float,
        iteration: int,
    ) -> list[dict]:
        span = self._layout_span(coordinates)
        step = span * 0.06 * learning_rate
        rng = random.Random(iteration * 9973 + 17)
        out = []
        for i, c in enumerate(coordinates):
            out.append({
                **c,
                "x": round(
                    float(c["x"]) + rng.uniform(-1, 1) * step,
                    4,
                ),
                "y": round(
                    float(c["y"]) + rng.uniform(-1, 1) * step,
                    4,
                ),
            })
        return out

    def _perturb_frequencies(
        self,
        G: nx.Graph,
        frequencies: dict[str, float],
        freq_range: tuple[float, float],
        iteration: int,
        strength: float,
    ) -> dict[str, float]:
        low, high = float(freq_range[0]), float(freq_range[1])
        rng = random.Random(iteration * 4447 + 3)
        nodes = list(G.nodes())
        if not nodes:
            return dict(frequencies)

        f = {str(k): float(v) for k, v in frequencies.items()}
        n_touch = max(1, len(nodes) // 4)
        for nid in rng.sample(nodes, min(n_touch, len(nodes))):
            nid = str(nid)
            base = f.get(nid, (low + high) / 2)
            delta = rng.uniform(-strength, strength)
            f[nid] = round(max(low, min(high, base + delta)), 4)
        return f

    def _repair_frequencies(
        self,
        G: nx.Graph,
        frequencies: dict[str, float],
        freq_range: tuple[float, float],
    ) -> dict[str, float]:
        """Fix only colliding pairs — do not reset the whole assignment."""
        low, high = float(freq_range[0]), float(freq_range[1])
        f = {str(k): float(v) for k, v in frequencies.items()}
        min_gap = self.physics.freq_collision_ghz + 0.005

        for _ in range(len(G.nodes()) * 2):
            issues = self.physics.check_frequency_collisions(G, f)
            if not issues:
                break
            issue = issues[0]
            u, v = issue["nodes"]
            if random.random() < 0.5:
                u, v = v, u
            if f.get(v, low) <= f.get(u, low):
                f[v] = round(min(high, f[u] + min_gap), 4)
            else:
                f[v] = round(max(low, f[u] - min_gap), 4)

        return f

    def _coord_map(self, coordinates: list[dict]) -> dict[str, tuple[float, float]]:
        return {
            str(c["id"]): (float(c["x"]), float(c["y"]))
            for c in coordinates
        }

    def _dist(self, pos: dict[str, tuple[float, float]], u: str, v: str) -> float:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        return math.hypot(x1 - x2, y1 - y2)

    def _ensure_connected(self, G: nx.Graph, pos: dict[str, tuple[float, float]]) -> nx.Graph:
        if G.number_of_nodes() <= 1 or nx.is_connected(G):
            return G
        H = G.copy()
        components = list(nx.connected_components(H))
        while len(components) > 1:
            best_d, best_pair = float("inf"), None
            for i in range(len(components)):
                for j in range(i + 1, len(components)):
                    for u in components[i]:
                        for v in components[j]:
                            u, v = str(u), str(v)
                            if u not in pos or v not in pos:
                                continue
                            d = self._dist(pos, u, v)
                            if d < best_d:
                                best_d, best_pair = d, (u, v)
            if not best_pair:
                break
            H.add_edge(best_pair[0], best_pair[1])
            components = list(nx.connected_components(H))
        return H

    def _evolve_topology(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        validation: dict[str, Any],
        iteration: int,
        lattice_type: str,
    ) -> nx.Graph:
        """
        Upgrade topology from validation feedback:
        - remove couplers that cause frequency crowding
        - add couplers when connectivity is below target
        - prune crowded non-essential links when spatial crosstalk is high
        """
        H = G.copy()
        n = H.number_of_nodes()
        if n < 2:
            return H

        metrics = validation.get("metrics", {})
        pos = self._coord_map(coordinates)
        rng = random.Random(iteration * 5521 + 7)
        target_conn = float(metrics.get("connectivity_target", 3.0))
        conn = float(metrics.get("connectivity_score", 0.0))
        min_edges = max(n - 1, 1)
        heavy_hex = "heavy" in lattice_type.lower()

        # Learn: drop bonds that fail frequency crowding checks
        for issue in metrics.get("freq_issues", []):
            u, v = str(issue["nodes"][0]), str(issue["nodes"][1])
            if H.has_edge(u, v) and H.number_of_edges() > min_edges:
                H.remove_edge(u, v)

        spatial = metrics.get("spatial_issues", [])
        if len(spatial) >= 2 and H.number_of_edges() > min_edges:
            removable = [
                (u, v)
                for u, v in H.edges()
                if H.degree(u) > 1 and H.degree(v) > 1
            ]
            if removable:
                u, v = rng.choice(removable)
                H.remove_edge(str(u), str(v))

        nodes = [str(nd) for nd in H.nodes() if str(nd) in pos]

        # Only heavy-hex targets ~3 connectivity; grid lattices keep designer topology
        if heavy_hex and conn < target_conn - 0.25:
            candidates: list[tuple[float, str, str]] = []
            for i, u in enumerate(nodes):
                for v in nodes[i + 1 :]:
                    if H.has_edge(u, v):
                        continue
                    if H.degree(u) >= self.MAX_DEGREE or H.degree(v) >= self.MAX_DEGREE:
                        continue
                    candidates.append((self._dist(pos, u, v), u, v))
            candidates.sort(key=lambda x: x[0])
            if candidates:
                _, u, v = candidates[0]
                H.add_edge(u, v)

        H = self._ensure_connected(H, pos)
        return H

    def _polish_state(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        frequencies: dict[str, float],
        freq_range: tuple[float, float],
        validation: dict[str, Any],
        lattice_type: str,
    ) -> tuple[nx.Graph, list[dict], dict[str, float]]:
        """Conservative improvement pass on the current champion."""
        coords = copy.deepcopy(coordinates)
        if len(coords) >= 2:
            coords = self.layout_optimizer.optimize_positions(G, coords)
        freqs = self._repair_frequencies(G, dict(frequencies), freq_range)
        G_out = self._evolve_topology(G, coords, validation, 0, lattice_type)
        self.physics.sync_coordinate_frequencies(coords, freqs)
        return G_out, coords, freqs

    def _propose_candidate(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        frequencies: dict[str, float],
        freq_range: tuple[float, float],
        iteration: int,
        learning_rate: float,
        validation: dict[str, Any],
        lattice_type: str,
        attempt: int,
    ) -> tuple[nx.Graph, list[dict], dict[str, float]]:
        """Small step from champion — always repair frequencies afterward."""
        coords = self._mutate_positions(
            coordinates, learning_rate * (0.85 ** attempt), iteration + attempt
        )
        if len(coords) >= 2:
            coords = self.layout_optimizer.optimize_positions(G, coords)

        span = self._layout_span(coords)
        strength = min(0.08, 0.03 + span * 0.008) * learning_rate
        freqs = self._perturb_frequencies(
            G, dict(frequencies), freq_range, iteration + attempt, strength=strength
        )
        freqs = self._repair_frequencies(G, freqs, freq_range)

        G_next = self._evolve_topology(
            G, coords, validation, iteration + attempt, lattice_type
        )
        self.physics.sync_coordinate_frequencies(coords, freqs)
        return G_next, coords, freqs

    def _evaluate(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        frequencies: dict[str, float],
        lattice_type: str,
    ) -> tuple[float, dict[str, Any]]:
        validation = self.validator.validate(
            G, coordinates, frequencies, lattice_type=lattice_type
        )
        score = self.compute_score(validation, validation.get("metrics", {}))
        return score, validation

    def _advance_champion(
        self,
        champion_G: nx.Graph,
        champion_coords: list[dict],
        champion_freqs: dict[str, float],
        champion_score: float,
        champion_validation: dict[str, Any],
        freq_range: tuple[float, float],
        iteration: int,
        learning_rate: float,
        lattice_type: str,
    ) -> tuple[nx.Graph, list[dict], dict[str, float], float, dict[str, Any]]:
        """Try to improve champion; keep it if no candidate beats it."""
        best_G = champion_G
        best_coords = champion_coords
        best_freqs = champion_freqs
        best_score = champion_score
        best_validation = champion_validation

        for attempt in range(4):
            cand_G, cand_coords, cand_freqs = self._propose_candidate(
                champion_G,
                champion_coords,
                champion_freqs,
                freq_range,
                iteration,
                learning_rate,
                champion_validation,
                lattice_type,
                attempt,
            )
            cand_score, cand_validation = self._evaluate(
                cand_G, cand_coords, cand_freqs, lattice_type
            )
            if cand_score > best_score + self.SCORE_EPS:
                best_G = cand_G
                best_coords = cand_coords
                best_freqs = cand_freqs
                best_score = cand_score
                best_validation = cand_validation

        if best_score <= champion_score + self.SCORE_EPS:
            polish_G, polish_coords, polish_freqs = self._polish_state(
                champion_G,
                champion_coords,
                champion_freqs,
                freq_range,
                champion_validation,
                lattice_type,
            )
            polish_score, polish_validation = self._evaluate(
                polish_G, polish_coords, polish_freqs, lattice_type
            )
            if polish_score > best_score + self.SCORE_EPS:
                best_G, best_coords, best_freqs = polish_G, polish_coords, polish_freqs
                best_score = polish_score
                best_validation = polish_validation

        return best_G, best_coords, best_freqs, best_score, best_validation

    def run_iterative(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        frequencies: dict[str, float],
        config: dict[str, Any],
    ) -> Iterator[dict[str, Any]]:
        """Yield champion state each iteration — scores trend upward (momentum)."""
        freq_range = tuple(config.get("freq_range", [4.5, 5.5]))
        lattice_type = config.get("lattice_type", "heavy_hex")

        champion_G = G.copy()
        champion_coords = copy.deepcopy(coordinates)
        champion_freqs = dict(frequencies)
        self.physics.sync_coordinate_frequencies(champion_coords, champion_freqs)

        champion_score, champion_validation = self._evaluate(
            champion_G, champion_coords, champion_freqs, lattice_type
        )
        champion_G, champion_coords, champion_freqs = self._polish_state(
            champion_G,
            champion_coords,
            champion_freqs,
            freq_range,
            champion_validation,
            lattice_type,
        )
        polish_score, polish_validation = self._evaluate(
            champion_G, champion_coords, champion_freqs, lattice_type
        )
        if polish_score >= champion_score - self.SCORE_EPS:
            champion_score, champion_validation = polish_score, polish_validation

        best_iteration = 1
        lr = 1.0
        converged = False
        min_iters = max(3, min(self.min_iterations, self.max_iterations))
        all_records: list[dict[str, Any]] = []
        seen_fingerprints: set[str] = set()
        seen_topologies: set[str] = set()
        prev_score = -1.0

        for iteration in range(1, self.max_iterations + 1):
            state_edges = _edges_from_graph(champion_G)
            validation = champion_validation
            metrics = validation.get("metrics", {})
            score = champion_score
            topo_fp = _topology_fingerprint(state_edges)
            fingerprint = _layout_fingerprint(
                champion_coords, champion_freqs, state_edges
            )

            improved = score > prev_score + self.SCORE_EPS
            if improved or iteration == 1:
                best_iteration = iteration

            record = {
                "type": "rl_iteration",
                "iteration": iteration,
                "score": score,
                "score_delta": round(score - prev_score, 1) if iteration > 1 else 0.0,
                "valid": validation.get("valid", False),
                "is_best": True,
                "best_score_so_far": score,
                "best_iteration_so_far": best_iteration,
                "errors": list(validation.get("errors", [])),
                "warnings": list(validation.get("warnings", [])),
                "layout_fingerprint": fingerprint,
                "topology_fingerprint": topo_fp,
                "layout_unique": fingerprint not in seen_fingerprints,
                "topology_unique": topo_fp not in seen_topologies,
                "edges": copy.deepcopy(state_edges),
                "n_edges": len(state_edges),
                "metrics": {
                    "crosstalk_estimate": metrics.get("crosstalk_estimate"),
                    "frequency_collisions": metrics.get("frequency_collisions"),
                    "spatial_crosstalk_flags": metrics.get("spatial_crosstalk_flags"),
                    "connectivity_score": metrics.get("connectivity_score"),
                    "layout_density": metrics.get("layout_density"),
                },
                "coordinates": copy.deepcopy(champion_coords),
                "frequencies": dict(champion_freqs),
                "validation": validation,
            }
            seen_fingerprints.add(fingerprint)
            seen_topologies.add(topo_fp)
            all_records.append(record)
            prev_score = score
            yield record

            can_stop_early = (
                iteration >= min_iters
                and validation.get("valid")
                and score >= self.target_score
            )
            if can_stop_early:
                converged = True
                break

            if iteration < self.max_iterations:
                champion_G, champion_coords, champion_freqs, champion_score, champion_validation = (
                    self._advance_champion(
                        champion_G,
                        champion_coords,
                        champion_freqs,
                        champion_score,
                        champion_validation,
                        freq_range,
                        iteration,
                        lr,
                        lattice_type,
                    )
                )
                lr = max(0.35, lr * 0.95)

        best_score = champion_score
        for r in all_records:
            r["is_best"] = r["iteration"] == best_iteration
            r["best_score_so_far"] = best_score
            r["best_iteration_so_far"] = best_iteration

        yield {
            "type": "rl_complete",
            "converged": converged,
            "best_iteration": best_iteration,
            "best_score": best_score,
            "iterations_run": len(all_records),
            "min_iterations": min_iters,
            "unique_layouts": len(seen_fingerprints),
            "unique_topologies": len(seen_topologies),
            "ranking": [
                {
                    "iteration": r["iteration"],
                    "score": r["score"],
                    "valid": r["valid"],
                    "errors": len(r["errors"]),
                    "bonds": r.get("n_edges", 0),
                    "topology": r.get("topology_fingerprint"),
                }
                for r in sorted(all_records, key=lambda x: x["score"], reverse=True)
            ],
        }

    def run(
        self,
        G: nx.Graph,
        coordinates: list[dict],
        frequencies: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        history: list[dict[str, Any]] = []
        best_coords = copy.deepcopy(coordinates)
        best_freqs = dict(frequencies)
        best_edges = _edges_from_graph(G)
        complete: dict[str, Any] = {}

        for event in self.run_iterative(G, coordinates, frequencies, config):
            if event["type"] == "rl_iteration":
                history.append({
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
            elif event["type"] == "rl_complete":
                complete = event
                best_it = complete.get("best_iteration")
                for h in history:
                    if h["iteration"] == best_it:
                        best_coords = copy.deepcopy(h["coordinates"])
                        best_freqs = dict(h["frequencies"])
                        best_edges = copy.deepcopy(h.get("edges", best_edges))
                        h["is_best"] = True
                    else:
                        h["is_best"] = False

        self.physics.sync_coordinate_frequencies(best_coords, best_freqs)
        return {
            "coordinates": best_coords,
            "frequencies": best_freqs,
            "edges": best_edges,
            "history": history,
            "best_iteration": complete.get("best_iteration", 1),
            "best_score": complete.get("best_score", 0),
            "converged": complete.get("converged", False),
            "final_valid": history[-1]["valid"] if history else False,
            "iterations_run": complete.get("iterations_run", len(history)),
            "unique_layouts": complete.get("unique_layouts", 0),
            "unique_topologies": complete.get("unique_topologies", 0),
        }
