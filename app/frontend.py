"""
Streamlit UI — live RL session with full iteration sweep and best-chip selection.
"""

from __future__ import annotations

import os
from typing import Any, Iterator

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components

from topo_architect.app.chip_fabricated_viz import render_fabricated_chip
from topo_architect.app.chip_viz import render_chip_dashboard

API_BASE = os.environ.get("TOPO_API_URL", "http://127.0.0.1:8000/api/v1")

st.set_page_config(
    page_title="Topo-Architect",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #030712 0%, #0a0f1e 100%); }
    h1 { color: #e0f4ff !important; }
    .best-banner {
        padding: 12px 16px; border-radius: 10px; margin: 12px 0;
        background: rgba(163,230,53,0.12); border: 1px solid rgba(163,230,53,0.45);
        color: #a3e635; font-family: monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI-Driven Topo-Architect")
st.caption("RL runs every iteration · compares all chip layouts · selects the best")


def api_get(path: str) -> dict:
    r = requests.get(f"{API_BASE}{path}", timeout=10)
    r.raise_for_status()
    return r.json()


def api_post(path: str, payload: dict) -> dict:
    r = requests.post(f"{API_BASE}{path}", json=payload, timeout=600)
    r.raise_for_status()
    return r.json()


def api_stream_design(payload: dict) -> Iterator[dict[str, Any]]:
    with requests.post(
        f"{API_BASE}/design/stream", json=payload, stream=True, timeout=900
    ) as r:
        r.raise_for_status()
        for raw in r.iter_lines(decode_unicode=True):
            if raw:
                yield __import__("json").loads(raw)


def iteration_chip_payload(base: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    return {
        "design_id": base.get("design_id"),
        "config": base.get("config", {}),
        "edges": event.get("edges") or base.get("edges", []),
        "coordinates": event.get("coordinates", []),
        "frequencies": event.get("frequencies", {}),
        "validation": event.get("validation", {}),
        "optimization": {
            "best_score": event.get("score"),
            "best_iteration": event.get("iteration"),
            "mode": "rl",
        },
    }


def _as_bool(value: Any) -> bool:
    """Coerce API/session values to bool for Streamlit expanded=."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "on")
    return False


def _is_best_iteration(ev: dict[str, Any], best_it: Any) -> bool:
    """True only when this RL iteration is the winner (strict bool for st.expander)."""
    if _as_bool(ev.get("is_best")):
        return True
    it = ev.get("iteration")
    if it is None or best_it is None:
        return False
    try:
        return int(it) == int(best_it)
    except (TypeError, ValueError):
        return str(it) == str(best_it)


with st.sidebar:
    st.header("System")
    try:
        health = api_get("/health")
        st.success("API connected")
        if health.get("ollama_available"):
            st.success("Ollama online")
        else:
            st.warning("Ollama offline")
    except requests.RequestException as e:
        st.error(str(e))

    st.divider()
    optimize = st.checkbox("RL optimize chip design", value=True)
    max_rl = st.slider("Max RL iterations", 5, 30, 15)
    min_rl = st.slider(
        "Min iterations before early stop",
        3,
        max_rl,
        max(5, max_rl // 2),
        help="RL always runs at least this many designs, then picks the best score.",
    )
    live_rl = st.checkbox("Live iteration updates", value=True)

    for ex in [
        "20 qubits heavy-hex 4.6 to 5.2 GHz",
        "16 qubits honeycomb layout",
        "9 qubits square grid",
    ]:
        if st.button(ex, key="ex_" + ex[:12]):
            st.session_state["prompt"] = ex

prompt = st.text_area(
    "Design prompt",
    value=st.session_state.get("prompt", "20 qubits heavy-hex 4.6 to 5.2 GHz"),
    height=90,
)

if st.button("Generate topology", type="primary"):
    payload = {
        "prompt": prompt,
        "optimize": optimize,
        "max_rl_iterations": max_rl,
        "min_rl_iterations": min_rl,
    }
    st.session_state["rl_iterations_ui"] = []
    st.session_state["result"] = None
    st.session_state["leaderboard"] = []

    try:
        if optimize and live_rl:
            progress = st.progress(0.0, text="Initializing…")
            status_line = st.empty()
            leaderboard_slot = st.empty()
            chip_slot = st.empty()
            base: dict[str, Any] = {}
            rows: list[dict[str, Any]] = []

            for event in api_stream_design(payload):
                et = event.get("type")
                if et == "status":
                    status_line.info(event.get("message", "…"))
                elif et == "error":
                    st.error(event.get("message"))
                    break
                elif et == "initial_design":
                    base = event
                    status_line.info("Topology built — starting RL iterations…")
                elif et == "rl_iteration":
                    it = event["iteration"]
                    delta = event.get("score_delta")
                    delta_str = (
                        f"+{delta}"
                        if isinstance(delta, (int, float)) and delta > 0
                        else ("—" if it == 1 else str(delta))
                    )
                    rows.append({
                        "Iteration": it,
                        "Score": event["score"],
                        "Δ": delta_str,
                        "Valid": event.get("valid"),
                        "Errors": len(event.get("errors") or []),
                        "Bonds": event.get("n_edges", len(event.get("edges") or [])),
                    })
                    progress.progress(
                        it / max_rl,
                        text=f"Running iteration {it} of {max_rl}…",
                    )
                    status_line.success(
                        f"Iteration **{it}/{max_rl}** · score **{event['score']}** · "
                        f"best so far: **{event.get('best_score_so_far')}** "
                        f"(iter {event.get('best_iteration_so_far')})"
                    )
                    leaderboard_slot.dataframe(
                        pd.DataFrame(rows),
                        use_container_width=True,
                        hide_index=True,
                    )
                    with chip_slot.container():
                        chip_data = iteration_chip_payload(base, event)
                        err_n = len(event.get("errors") or [])
                        st.markdown(
                            f"#### Iteration {it} — score {event['score']} "
                            f"{'★ best' if _is_best_iteration(event, event.get('best_iteration_so_far')) else ''}"
                            + (f" · errors {err_n}" if err_n else "")
                        )
                        if event.get("errors"):
                            for msg in event["errors"][:4]:
                                st.caption(f"⚠ {msg}")
                        components.html(
                            render_fabricated_chip(chip_data),
                            height=620,
                            scrolling=True,
                        )
                    st.session_state["rl_iterations_ui"].append(
                        {"event": event, "chip_data": iteration_chip_payload(base, event)}
                    )
                elif et == "rl_complete":
                    progress.progress(1.0, text="Selecting best design…")
                    status_line.success(
                        f"Completed **{event.get('iterations_run')}** iterations · "
                        f"★ Best: **iteration {event.get('best_iteration')}** · "
                        f"score **{event.get('best_score')}**"
                    )
                    if event.get("ranking"):
                        st.session_state["leaderboard"] = event["ranking"]
                elif et == "final":
                    st.session_state["result"] = event["result"]
                    progress.progress(1.0, text="Done")

        else:
            with st.spinner("Running pipeline…"):
                st.session_state["result"] = api_post("/design", payload)
    except requests.RequestException as e:
        st.error(str(e))

result: dict[str, Any] | None = st.session_state.get("result")

if result:
    opt = result.get("optimization", {})
    validation = result.get("validation", {})
    config = result.get("config", {})
    best_it = opt.get("best_iteration")
    best_score = opt.get("best_score")

    st.markdown(
        f'<div class="best-banner">★ WINNER — Iteration {best_it} · RL Score {best_score} · '
        f'Chosen from {opt.get("iterations_run", "—")} candidate chip layouts</div>',
        unsafe_allow_html=True,
    )

    ranking = opt.get("ranking") or st.session_state.get("leaderboard") or []
    if ranking:
        st.markdown("##### Score ranking (all iterations)")
        st.dataframe(pd.DataFrame(ranking), use_container_width=True, hide_index=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Qubits", config.get("qubits"))
    c2.metric("Best score", best_score)
    c3.metric("Best iteration", best_it)
    c4.metric("Valid", "✓" if validation.get("valid") else "✗")

    t_topo, t_fab, t_iters, t_report = st.tabs(
        [
            "Topology map",
            "★ Fabricated chip",
            "All RL iterations",
            "Report & exports",
        ]
    )

    with t_topo:
        if result.get("coordinates"):
            components.html(render_chip_dashboard(result), height=650, scrolling=True)

    with t_fab:
        st.caption(
            "Qiskit Metal style — TransmonPocket · RouteMeander readout · LaunchpadWirebond"
        )
        if result.get("coordinates"):
            components.html(render_fabricated_chip(result), height=660, scrolling=True)
        py_path = result.get("export_paths", {}).get("metal_script")
        if py_path and os.path.isfile(py_path):
            with st.expander("Generated Qiskit Metal Python script"):
                st.code(open(py_path, encoding="utf-8").read(), language="python")

    with t_iters:
        hist = opt.get("rl_history") or []
        if hist:
            st.line_chart(
                pd.DataFrame({"iteration": [h["iteration"] for h in hist], "score": [h["score"] for h in hist]}),
                x="iteration",
                y="score",
            )
        ui_iters = st.session_state.get("rl_iterations_ui") or []
        source = ui_iters if ui_iters else [
            {
                "event": h,
                "chip_data": {
                    "config": config,
                    "edges": h.get("edges") or result.get("edges"),
                    "coordinates": h.get("coordinates"),
                    "frequencies": h.get("frequencies"),
                    "validation": validation,
                    "optimization": {"best_score": h["score"]},
                },
            }
            for h in hist
        ]
        for item in source:
            ev = item["event"]
            is_best = _is_best_iteration(ev, best_it)
            with st.expander(
                f"Iteration {ev.get('iteration')} — score {ev.get('score')}"
                + (" ★ BEST" if is_best else ""),
                expanded=is_best,
            ):
                err_n = len(ev.get("errors") or [])
                if err_n:
                    st.caption(f"Errors: {err_n}")
                components.html(render_fabricated_chip(item["chip_data"]), height=520)

    with t_report:
        st.markdown(result.get("report_markdown", ""))
        for label, path in (result.get("export_paths") or {}).items():
            if path and os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    st.download_button(f"Download {label}", f.read(), os.path.basename(path))
