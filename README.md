# AI-Driven Topo-Architect

Local-first, multi-agent quantum chip topology design using **Ollama**, **NetworkX**, **FastAPI**, **Streamlit**, and **Qiskit Metal**.

## Architecture

```
Streamlit UI  <-->  FastAPI API  -->  Agent Orchestrator
                                         |
    Analyst | Designer | Validator | Optimizer | Reporter
                                         |
                              Quantum Design Engine (NetworkX / Metal)
                                         |
                              Export (JSON / Markdown / Metal script)
```

## Requirements

| Install file | Python | Includes Metal/GDS |
|--------------|--------|-------------------|
| `requirements-core.txt` | **3.11–3.13** | No |
| `requirements-metal.txt` | **3.10 only** | Yes |

- [Ollama](https://ollama.ai) (optional; offline fallback works)
- **Python 3.13 users:** use `requirements-core.txt` — do not pin `numpy==1.26.4` (no Windows wheel; needs MSVC to compile)
- **Qiskit Metal:** install [Python 3.10](https://www.python.org/downloads/release/python-31011/) + Visual Studio Build Tools

## Quick start

From the repository root (`QuantumChipAssistant`):

```powershell
cd topo_architect
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements-core.txt
```

On **Python 3.10** only (Metal/GDS):

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements-metal.txt
```

Default `requirements.txt` points at the core stack:

```powershell
pip install -r requirements.txt
```

Start API:

```powershell
cd ..
$env:PYTHONPATH = (Get-Location).Path
uvicorn topo_architect.app.main:app --reload --port 8000
```

Start UI (second terminal):

```powershell
$env:PYTHONPATH = (Get-Location).Path
streamlit run topo_architect/app/frontend.py
```

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Ollama + service status |
| `/api/v1/design` | POST | Full multi-agent pipeline |
| `/api/v1/lattice/preview` | POST | Graph-only preview |

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/design \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"100 qubits heavy-hex layout\", \"optimize\": true}"
```

## Tests

```powershell
pytest topo_architect/tests -q
```

## Legacy app

The original Flask **QuantumForge** prototype (`app.py`, `index.html`) remains in the repo root for RL-driven transmon optimization demos.

## Hackathon MVP order

1. Graph generation + Streamlit
2. Analyst + Validator
3. Physics scoring
4. Plotly map + exports
5. Ollama + Metal GDS (when environment supports it)
