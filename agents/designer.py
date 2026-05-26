"""Agent 2: JSON config → NetworkX graph + coordinates."""

from __future__ import annotations

from typing import Any

import networkx as nx

from topo_architect.quantum_core.generators import graph_to_coordinates, lattice_from_type
from topo_architect.models.llm_client import OllamaClient, get_llm_client, pick_model


class DesignerAgent:
    PREFERRED_MODELS = ["llama3.2", "deepseek-coder:6.7b", "qwen2.5-coder", "gpt-oss:120b"]

    def __init__(self, llm: OllamaClient | None = None, model: str | None = None):
        self.llm = llm or get_llm_client()
        self.model = model or pick_model(self.llm, self.PREFERRED_MODELS)

    def design(self, config: dict[str, Any]) -> dict[str, Any]:
        n = config.get("qubits", 16)
        lattice = config.get("lattice_type", "heavy_hex")
        dims = config.get("dimensions")
        dim_tuple = tuple(dims) if dims and len(dims) >= 2 else None

        G = lattice_from_type(lattice, n, dimensions=dim_tuple)
        coordinates = graph_to_coordinates(G, spacing=1.0)

        edges = [{"source": str(u), "target": str(v)} for u, v in G.edges()]
        return {
            "graph": G,
            "coordinates": coordinates,
            "edges": edges,
            "n_nodes": G.number_of_nodes(),
            "n_edges": G.number_of_edges(),
            "lattice_type": lattice,
        }

    def suggest_layout_tweaks(self, config: dict, metrics: dict) -> str:
        """Optional LLM commentary on layout (uses deepseek when available)."""
        if not self.llm.is_available():
            return "Rule-based layout applied (Ollama offline)."
        prompt = (
            f"Config: {config}\nMetrics: {metrics}\n"
            "Give 2 bullet tips to improve this superconducting qubit layout."
        )
        try:
            return self.llm.generate(
                prompt,
                model=pick_model(self.llm, self.PREFERRED_MODELS),
                temperature=0.3,
            )
        except Exception:
            return "Designer LLM unavailable."
