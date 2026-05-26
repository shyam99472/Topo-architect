"""Agent 5: Markdown report + export artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from topo_architect.models.llm_client import OllamaClient, get_llm_client, pick_model
from topo_architect.quantum_core.metal_interface import generate_metal_script


class ReporterAgent:
    def __init__(
        self,
        llm: OllamaClient | None = None,
        model: str | None = None,
        export_dir: str | Path | None = None,
    ):
        self.llm = llm or get_llm_client()
        self.PREFERRED_MODELS = ["llama3.2", "mistral", "gemma3", "gpt-oss:120b"]
        self.model = model or pick_model(self.llm, self.PREFERRED_MODELS)
        self.export_dir = Path(export_dir or Path(__file__).resolve().parents[1] / "exports")
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def build_report(
        self,
        config: dict,
        design: dict,
        validation: dict,
        optimization: dict,
        user_prompt: str = "",
    ) -> str:
        metrics = validation.get("metrics", {})
        lines = [
            "# AI-Driven Topo-Architect — Design Report",
            "",
            f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            "## User Request",
            f"> {user_prompt or config.get('notes', 'N/A')}",
            "",
            "## Design Summary",
            f"- **Qubits:** {config.get('qubits')}",
            f"- **Lattice:** {config.get('lattice_type')}",
            f"- **Nodes / Edges:** {design.get('n_nodes')} / {design.get('n_edges')}",
            f"- **Frequency range (GHz):** {config.get('freq_range')}",
            "",
            "## Physics Metrics",
            f"- **Connectivity score (E/V):** {metrics.get('connectivity_score', '—')}",
            f"- **Layout density:** {metrics.get('layout_density', '—')}",
            f"- **Crosstalk estimate:** {metrics.get('crosstalk_estimate', '—')}",
            f"- **Frequency collisions:** {metrics.get('frequency_collisions', 0)}",
            f"- **Spatial crosstalk flags:** {metrics.get('spatial_crosstalk_flags', 0)}",
            "",
            "## Optimization",
            f"- **Mode:** {optimization.get('mode', 'none')}",
            f"- **Crosstalk before:** {optimization.get('crosstalk_before', '—')}",
            f"- **Crosstalk after:** {optimization.get('crosstalk_after', '—')}",
            f"- **Improvement:** {optimization.get('improvement_pct', 0)}%",
        ]
        if optimization.get("mode") == "rl":
            lines += [
                f"- **RL iterations:** {optimization.get('iterations_run', '—')}",
                f"- **Best RL score:** {optimization.get('best_score', '—')} (iter {optimization.get('best_iteration', '—')})",
                f"- **Converged:** {optimization.get('converged', False)}",
                "",
            ]
        lines += [
            "",
            "## Validation",
            f"- **Status:** {'PASS' if validation.get('valid') else 'ISSUES FOUND'}",
        ]
        if validation.get("errors"):
            lines.append("### Errors")
            for e in validation["errors"]:
                lines.append(f"- {e}")
        if validation.get("warnings"):
            lines.append("### Warnings")
            for w in validation["warnings"]:
                lines.append(f"- {w}")

        narrative = self._llm_narrative(config, metrics, validation.get("valid", False))
        if narrative:
            lines.extend(["", "## AI Analysis", narrative])

        return "\n".join(lines)

    def _llm_narrative(self, config: dict, metrics: dict, valid: bool) -> str:
        if not self.llm.is_available():
            return "_Ollama offline — report uses computed metrics only._"
        try:
            return self.llm.generate(
                prompt=(
                    f"Summarize this quantum chip layout in 3 sentences for an engineer.\n"
                    f"Config: {config}\nMetrics: {metrics}\nValid: {valid}"
                ),
                model=pick_model(self.llm, self.PREFERRED_MODELS),
                temperature=0.4,
            )
        except Exception:
            return ""

    def export_artifacts(
        self,
        design_id: str,
        config: dict,
        coordinates: list[dict],
        edges: list[dict],
        report_md: str,
        frequencies: dict[str, float],
    ) -> dict[str, str]:
        """Write JSON summary, Markdown report, and Qiskit Metal script."""
        paths = {}
        base = self.export_dir / design_id
        base.mkdir(parents=True, exist_ok=True)

        json_path = base / "design.json"
        summary = {
            "design_id": design_id,
            "config": config,
            "coordinates": coordinates,
            "edges": edges,
            "frequencies": frequencies,
        }
        json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        paths["json"] = str(json_path)

        md_path = base / "report.md"
        md_path.write_text(report_md, encoding="utf-8")
        paths["markdown"] = str(md_path)

        script = generate_metal_script(
            coordinates, design_name=design_id, edges=edges
        )
        py_path = base / "metal_design.py"
        py_path.write_text(script, encoding="utf-8")
        paths["metal_script"] = str(py_path)

        return paths
