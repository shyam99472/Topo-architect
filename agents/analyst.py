"""Agent 1: NLP → design constraints JSON."""

from __future__ import annotations

import re
from typing import Any

from topo_architect.models.llm_client import OllamaClient, get_llm_client, pick_model

SYSTEM_PROMPT = """You are a quantum chip design analyst.
Extract design constraints from user text and return ONLY valid JSON with keys:
- qubits (int)
- lattice_type (one of: square, honeycomb, heavy_hex)
- dimensions ([rows, cols] or null)
- freq_range ([low_ghz, high_ghz])
- notes (short string)
Example: {"qubits": 16, "lattice_type": "heavy_hex", "dimensions": null, "freq_range": [4.5, 5.5], "notes": ""}
"""


class AnalystAgent:
    PREFERRED_MODELS = ["llama3.2", "llama3.1", "llama3:8b", "gemma3", "gpt-oss:120b"]

    def __init__(self, llm: OllamaClient | None = None, model: str | None = None):
        self.llm = llm or get_llm_client()
        self.model = model or pick_model(self.llm, self.PREFERRED_MODELS)

    def parse(self, user_text: str) -> dict[str, Any]:
        fallback = self._rule_based_parse(user_text)
        if not self.llm.is_available():
            return fallback

        try:
            result = self.llm.generate_json(
                prompt=f"User request:\n{user_text}",
                model=pick_model(self.llm, self.PREFERRED_MODELS),
                system=SYSTEM_PROMPT,
                fallback=fallback,
            )
            return self._normalize(result, fallback)
        except (ValueError, OSError, Exception):
            return fallback

    def _rule_based_parse(self, text: str) -> dict[str, Any]:
        tl = text.lower()
        qubits = 16
        for m in re.finditer(r"(\d+)\s*[- ]?qubit", tl):
            qubits = int(m.group(1))
            break
        else:
            for m in re.finditer(r"\b(\d{1,3})\b", tl):
                n = int(m.group(1))
                if 2 <= n <= 500:
                    qubits = n
                    break

        lattice = "heavy_hex"
        if "square" in tl or "grid" in tl:
            lattice = "square"
        elif "honeycomb" in tl or "hexagonal" in tl and "heavy" not in tl:
            lattice = "honeycomb"
        elif "heavy" in tl or "ibm" in tl:
            lattice = "heavy_hex"

        freq_low, freq_high = 4.5, 5.5
        if "low noise" in tl:
            freq_low, freq_high = 4.8, 5.2

        return {
            "qubits": qubits,
            "lattice_type": lattice,
            "dimensions": None,
            "freq_range": [freq_low, freq_high],
            "notes": text[:200],
        }

    def _normalize(self, data: dict, fallback: dict) -> dict[str, Any]:
        out = dict(fallback)
        if "qubits" in data:
            try:
                out["qubits"] = max(2, min(500, int(data["qubits"])))
            except (TypeError, ValueError):
                pass
        if "lattice_type" in data:
            lt = str(data["lattice_type"]).lower().replace("-", "_")
            if lt in ("square", "honeycomb", "heavy_hex", "grid", "hex"):
                out["lattice_type"] = "square" if lt == "grid" else (
                    "honeycomb" if lt == "hex" else lt
                )
        if "freq_range" in data and isinstance(data["freq_range"], (list, tuple)):
            if len(data["freq_range"]) >= 2:
                out["freq_range"] = [float(data["freq_range"][0]), float(data["freq_range"][1])]
        if data.get("dimensions"):
            out["dimensions"] = data["dimensions"]
        if data.get("notes"):
            out["notes"] = str(data["notes"])[:300]
        return out
