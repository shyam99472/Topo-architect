"""FastAPI route handlers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
from pydantic import BaseModel, Field

from topo_architect.agents.orchestrator import AgentOrchestrator
from topo_architect.models.llm_client import get_llm_client
from topo_architect.quantum_core.generators import lattice_from_type, graph_to_coordinates

router = APIRouter()
_orchestrator: Optional[AgentOrchestrator] = None


def get_orchestrator() -> AgentOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator


class DesignRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="Natural language chip design request")
    optimize: bool = True
    max_rl_iterations: int = Field(15, ge=3, le=50)
    min_rl_iterations: int | None = Field(None, ge=3, le=50)


class LatticeRequest(BaseModel):
    lattice_type: str = "heavy_hex"
    qubits: int = Field(16, ge=2, le=500)
    rows: Optional[int] = None
    cols: Optional[int] = None


@router.get("/health")
def health() -> dict[str, Any]:
    llm = get_llm_client()
    ollama = llm.status()
    return {
        "status": "ok",
        "service": "topo-architect",
        "ollama_available": ollama["available"],
        "ollama_models": ollama.get("models") or [],
        "ollama": ollama,
    }


@router.post("/design")
def create_design(req: DesignRequest) -> dict[str, Any]:
    try:
        orch = get_orchestrator()
        if req.min_rl_iterations:
            orch.rl_optimizer.min_iterations = req.min_rl_iterations
        return orch.run(
            req.prompt,
            optimize=req.optimize,
            max_rl_iterations=req.max_rl_iterations,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/design/stream")
def create_design_stream(req: DesignRequest):
    """NDJSON stream: one event per RL iteration, then final result."""

    def generate():
        try:
            orch = get_orchestrator()
            if req.min_rl_iterations:
                orch.rl_optimizer.min_iterations = req.min_rl_iterations
            for event in orch.run_streaming(
                req.prompt,
                optimize=req.optimize,
                max_rl_iterations=req.max_rl_iterations,
                min_rl_iterations=req.min_rl_iterations,
            ):
                yield json.dumps(event, default=str) + "\n"
        except Exception as exc:
            yield json.dumps({"type": "error", "message": str(exc)}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")


@router.post("/lattice/preview")
def lattice_preview(req: LatticeRequest) -> dict[str, Any]:
    dims = (req.rows, req.cols) if req.rows and req.cols else None
    G = lattice_from_type(req.lattice_type, req.qubits, dimensions=dims)
    coords = graph_to_coordinates(G)
    return {
        "lattice_type": req.lattice_type,
        "qubits": len(coords),
        "coordinates": coords,
        "edges": [{"source": str(u), "target": str(v)} for u, v in G.edges()],
    }


@router.get("/exports/{design_id}/{filename}")
def get_export(design_id: str, filename: str):
    base = Path(__file__).resolve().parents[2] / "exports" / design_id
    path = base / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Export not found")
    media = "application/json" if filename.endswith(".json") else "text/plain"
    if filename.endswith(".md"):
        media = "text/markdown"
    elif filename.endswith(".py"):
        media = "text/x-python"
    return FileResponse(path, media_type=media, filename=filename)


@router.get("/report/{design_id}")
def get_report(design_id: str):
    path = Path(__file__).resolve().parents[2] / "exports" / design_id / "report.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return PlainTextResponse(path.read_text(encoding="utf-8"))
