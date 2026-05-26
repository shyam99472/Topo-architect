"""
FastAPI entry point for AI-Driven Topo-Architect.

Run: uvicorn topo_architect.app.main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from topo_architect.app.api.routes import router
from topo_architect.models.llm_client import get_llm_client, get_ollama_config

app = FastAPI(
    title="AI-Driven Topo-Architect",
    description="Multi-agent quantum chip topology design API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
def _log_ollama_startup() -> None:
    cfg = get_ollama_config()
    st = get_llm_client().status()
    print(
        f"[topo-architect] Ollama: host={cfg['base_url']} "
        f"key={'yes' if cfg['api_key'] else 'NO'} "
        f"online={st['available']} "
        f"env={cfg['env_file'] or 'none'}"
    )
    if st.get("error"):
        print(f"[topo-architect] Ollama error: {st['error']}")


@app.get("/")
def root():
    return {
        "service": "topo-architect",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("topo_architect.app.main:app", host="0.0.0.0", port=8000, reload=True)
