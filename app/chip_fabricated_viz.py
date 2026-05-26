"""Fabricated chip view — spaced layout, orthogonal meanders, topology-accurate couplers."""

from __future__ import annotations

import html
import math
from typing import Any

import networkx as nx

# Visual constants (px) — keep centers far enough apart for clear gaps
QUBIT_W = 46
QUBIT_H = 46
READOUT_COMB_H = 16
QUBIT_RADIUS = 32  # inset for traces leaving pocket
MIN_CENTER_GAP = 98  # ~52px clear gap between qubit boxes


def _qubit_label(node_id: str, index: int) -> str:
    nid = str(node_id)
    if nid.lower().startswith("q"):
        num = nid[1:]
        if num.isdigit():
            return f"Q{num}"
    return f"Q{index}"


def _build_graph(coords: list[dict], edges: list[dict]) -> tuple[nx.Graph, dict[str, int]]:
    G = nx.Graph()
    id_to_idx: dict[str, int] = {}
    for i, c in enumerate(coords):
        nid = str(c["id"])
        id_to_idx[nid] = i
        G.add_node(nid)
    for e in edges:
        u, v = str(e["source"]), str(e["target"])
        if u in id_to_idx and v in id_to_idx:
            G.add_edge(u, v)
    return G, id_to_idx


def _canvas_size(n: int) -> tuple[float, float]:
    base_w, base_h = 760, 560
    extra = max(0, n - 6)
    return base_w + extra * 28, base_h + extra * 22


def _enforce_min_spacing(
    positions: list[tuple[float, float, int, int]], min_gap: float
) -> list[tuple[float, float, int, int]]:
    """Push qubit centers apart so pockets never overlap."""
    pts = [list(p) for p in positions]
    n = len(pts)
    for _ in range(80):
        moved = False
        for i in range(n):
            for j in range(i + 1, n):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                dist = math.hypot(dx, dy) or 0.01
                if dist >= min_gap:
                    continue
                push = (min_gap - dist) / 2 + 0.5
                ux, uy = dx / dist, dy / dist
                pts[i][0] -= ux * push
                pts[i][1] -= uy * push
                pts[j][0] += ux * push
                pts[j][1] += uy * push
                moved = True
        if not moved:
            break
    return [(p[0], p[1], p[2], p[3]) for p in pts]


def _fit_positions_to_canvas(
    positions: list[tuple[float, float, int, int]], w: float, h: float, pad: float
) -> list[tuple[float, float, int, int]]:
    if not positions:
        return []
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(max_x - min_x, 1.0)
    span_y = max(max_y - min_y, 1.0)
    scale = min((w - 2 * pad) / span_x, (h - 2 * pad) / span_y)
    cx, cy = (min_x + max_x) / 2, (min_y + max_y) / 2
    out = []
    for x, y, gi, gj in positions:
        nx_pos = w / 2 + (x - cx) * scale
        ny_pos = h / 2 + (y - cy) * scale
        out.append((nx_pos, ny_pos, gi, gj))
    return out


def _layout_positions(
    coords: list[dict], edges: list[dict], w: float, h: float
) -> list[tuple[float, float, int, int]]:
    """Place qubits with generous spacing; use design x,y when available."""
    n = len(coords)
    if n == 0:
        return []

    pad = 110
    G, _ = _build_graph(coords, edges)

    has_xy = all(c.get("x") is not None and c.get("y") is not None for c in coords)
    raw: list[tuple[float, float, int, int]] = []

    if has_xy:
        for i, c in enumerate(coords):
            raw.append((float(c["x"]), float(c["y"]), i % 3, i // 3))
    elif G.number_of_edges() > 0:
        k = max(3.8, 5.5 / math.sqrt(max(n, 1)))
        pos = nx.spring_layout(G, seed=42, k=k, iterations=150, scale=2.5)
        for i, c in enumerate(coords):
            px, py = pos[str(c["id"])]
            raw.append((float(px), float(py), i % 3, i // 3))
    else:
        cols = min(4, max(2, int(math.ceil(math.sqrt(n)))))
        for i in range(n):
            raw.append((i % cols, i // cols, i % cols, i // cols))

    # Spread in layout space before scaling to canvas
    spread = 2.4 if has_xy else 1.8
    raw = [(x * spread, y * spread, gi, gj) for x, y, gi, gj in raw]
    raw = _enforce_min_spacing(raw, spread * 1.05)
    fitted = _fit_positions_to_canvas(raw, w, h, pad)
    return _enforce_min_spacing(fitted, MIN_CENTER_GAP)


def _edge_index_pairs(edges: list[dict], id_to_idx: dict[str, int]) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for e in edges:
        u, v = str(e["source"]), str(e["target"])
        if u not in id_to_idx or v not in id_to_idx:
            continue
        i, j = id_to_idx[u], id_to_idx[v]
        key = (min(i, j), max(i, j))
        if key not in seen:
            seen.add(key)
            pairs.append(key)
    return pairs


def _build_adjacency_lines(coords: list[dict], edges: list[dict]) -> list[str]:
    G, id_to_idx = _build_graph(coords, edges)
    lines = []
    for nid in sorted(G.nodes(), key=lambda node: id_to_idx.get(node, 0)):
        neighbors = sorted(G.neighbors(nid), key=lambda node: id_to_idx.get(node, 0))
        lbl = _qubit_label(nid, id_to_idx[nid])
        nbrs = ", ".join(_qubit_label(nb, id_to_idx[nb]) for nb in neighbors) or "—"
        lines.append(f"{lbl} ↔ {nbrs}")
    return lines


def _inset_point(x1: float, y1: float, x2: float, y2: float, inset: float) -> tuple[float, float]:
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy) or 1.0
    ux, uy = dx / dist, dy / dist
    return x1 + ux * inset, y1 + uy * inset


def _route_meander_orthogonal(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    inset: float = QUBIT_RADIUS,
    leg: float = 18.0,
) -> str:
    """
  90° Manhattan meander (RouteMeander style) between two qubit centers.
  """
    sx, sy = _inset_point(x1, y1, x2, y2, inset)
    ex, ey = _inset_point(x2, y2, x1, y1, inset)

    points: list[tuple[float, float]] = [(sx, sy)]
    x, y = sx, sy
    rem_x, rem_y = ex - sx, ey - sy
    horiz = abs(rem_x) >= abs(rem_y)

    guard = 0
    while (abs(rem_x) > 1.5 or abs(rem_y) > 1.5) and guard < 40:
        guard += 1
        if horiz:
            step = leg if rem_x > 0 else -leg
            if abs(step) > abs(rem_x):
                step = rem_x
            x += step
            rem_x -= step
        else:
            step = leg if rem_y > 0 else -leg
            if abs(step) > abs(rem_y):
                step = rem_y
            y += step
            rem_y -= step
        points.append((x, y))
        horiz = not horiz

    points.append((ex, ey))
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in points)


def _readout_meander(
    qx: float,
    qy: float,
    lx: float,
    ly: float,
    inset: float = QUBIT_RADIUS,
    leg: float = 16.0,
) -> str:
    """Long serpentine readout from qubit to launchpad (more legs than coupler)."""
    sx, sy = _inset_point(qx, qy, lx, ly, inset + 6)
    return _route_meander_orthogonal(sx, sy, lx, ly, inset=0, leg=leg)


def _coupler_midpoint_on_path(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
    sx, sy = _inset_point(x1, y1, x2, y2, QUBIT_RADIUS)
    ex, ey = _inset_point(x2, y2, x1, y1, QUBIT_RADIUS)
    return (sx + ex) / 2, (sy + ey) / 2


def _nearest_launchpad(
    qx: float, qy: float, launch_map: list[tuple[float, float, float]]
) -> tuple[float, float, float]:
    best = launch_map[0]
    best_d = float("inf")
    for lp in launch_map:
        d = (qx - lp[0]) ** 2 + (qy - lp[1]) ** 2
        if d < best_d:
            best_d = d
            best = lp
    return best


def _launchpad_polygon(lx: float, ly: float, angle_deg: float, size: float = 28) -> str:
    a = math.radians(angle_deg)
    tip_x = lx + math.cos(a) * size * 1.12
    tip_y = ly + math.sin(a) * size * 1.12
    bx = lx - math.cos(a) * size * 0.22
    by = ly - math.sin(a) * size * 0.22
    px, py = -math.sin(a) * size * 0.38, math.cos(a) * size * 0.38
    return f"{tip_x:.1f},{tip_y:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}"


def render_fabricated_chip(result: dict[str, Any]) -> str:
    coords = result.get("coordinates") or []
    edges = result.get("edges") or []
    n = len(coords)
    if n == 0:
        return "<p>No design data</p>"

    _, id_to_idx = _build_graph(coords, edges)
    labels = [_qubit_label(c["id"], i) for i, c in enumerate(coords)]

    chip_w, chip_h = _canvas_size(n)
    positions = _layout_positions(coords, edges, chip_w, chip_h)
    pairs = _edge_index_pairs(edges, id_to_idx)

    frame_pad = 52
    launch_map = [
        (chip_w * 0.5, frame_pad, 90),
        (chip_w * 0.5, chip_h - frame_pad, 270),
        (frame_pad, chip_h * 0.5, 180),
        (chip_w - frame_pad, chip_h * 0.5, 0),
    ]
    # Extra corner launchpads for larger chips
    if n > 6:
        launch_map.extend([
            (frame_pad + 20, frame_pad + 20, 135),
            (chip_w - frame_pad - 20, frame_pad + 20, 45),
            (frame_pad + 20, chip_h - frame_pad - 20, 225),
            (chip_w - frame_pad - 20, chip_h - frame_pad - 20, 315),
        ])

    coupler_lines: list[str] = []
    for i, j in pairs:
        x1, y1, _, _ = positions[i]
        x2, y2, _, _ = positions[j]
        dist = math.hypot(x2 - x1, y2 - y1)
        leg = max(14, min(22, dist * 0.09))
        pts = _route_meander_orthogonal(x1, y1, x2, y2, leg=leg)
        mx, my = _coupler_midpoint_on_path(x1, y1, x2, y2)
        coupler_lines.append(
            f'<polyline points="{pts}" fill="none" stroke="#67d4ff" stroke-width="2.4" '
            f'stroke-linecap="square" stroke-linejoin="miter" filter="url(#glow)"/>'
            f'<rect x="{mx-6:.0f}" y="{my-6:.0f}" width="12" height="12" rx="1.5" '
            f'fill="#0a2038" stroke="#5ecfff" stroke-width="1.2"/>'
        )

    readout_lines: list[str] = []
    for i, (qx, qy, _, _) in enumerate(positions):
        lx, ly, ang = _nearest_launchpad(qx, qy, launch_map)
        pts = _readout_meander(qx, qy, lx, ly, leg=15)
        readout_lines.append(
            f'<polyline points="{pts}" fill="none" stroke="#4a9ec8" stroke-width="1.6" '
            f'stroke-linecap="square" stroke-linejoin="miter" opacity="0.85"/>'
        )

    launch_svgs = [
        f'<polygon points="{_launchpad_polygon(lx, ly, ang)}" fill="#081420" stroke="#78d4ff" stroke-width="1.3"/>'
        for lx, ly, ang in launch_map[:4]
    ]

    qubit_svgs: list[str] = []
    bw, bh = QUBIT_W, QUBIT_H
    comb_top = READOUT_COMB_H + 4
    for i, (cx, cy, _, _) in enumerate(positions):
        lbl = labels[i]
        freq = float(coords[i].get("frequency_ghz") or 0) if i < len(coords) else 0
        top_y = cy - bh / 2 - comb_top

        qubit_svgs.append(
            f'<rect x="{cx-bw/2:.0f}" y="{top_y:.0f}" width="{bw}" height="10" rx="2" '
            f'fill="none" stroke="#5aafc8" stroke-width="0.9"/>'
        )
        for t in range(5):
            tx = cx - 12 + t * 6
            qubit_svgs.append(
                f'<line x1="{tx:.0f}" y1="{top_y+2:.0f}" x2="{tx:.0f}" y2="{top_y+9:.0f}" '
                f'stroke="#6ecfff" stroke-width="0.9"/>'
            )
        qubit_svgs.append(
            f'<rect x="{cx-bw/2:.0f}" y="{cy-bh/2:.0f}" width="{bw}" height="{bh}" rx="4" '
            f'fill="#0a1624" stroke="#8ee8ff" stroke-width="2" filter="url(#boxGlow)"/>'
        )
        for bar in range(3):
            qubit_svgs.append(
                f'<rect x="{cx-14:.0f}" y="{cy-8+bar*8:.0f}" width="28" height="3" rx="1" '
                f'fill="#1a4060" stroke="#5a9ec0" stroke-width="0.5"/>'
            )
        qubit_svgs.append(
            f'<line x1="{cx-6:.0f}" y1="{cy-6:.0f}" x2="{cx+6:.0f}" y2="{cy+6:.0f}" stroke="#b8f0ff" stroke-width="1.4"/>'
            f'<line x1="{cx+6:.0f}" y1="{cy-6:.0f}" x2="{cx-6:.0f}" y2="{cy+6:.0f}" stroke="#b8f0ff" stroke-width="1.4"/>'
        )
        qubit_svgs.append(
            f'<text x="{cx:.0f}" y="{cy+4:.0f}" fill="#ffffff" font-size="14" text-anchor="middle" '
            f'font-family="Orbitron,Arial,sans-serif" font-weight="700">{lbl}</text>'
        )
        if freq > 0:
            qubit_svgs.append(
                f'<text x="{cx:.0f}" y="{cy+bh/2+14:.0f}" fill="#6ecfff" font-size="7" '
                f'text-anchor="middle" font-family="monospace">{freq:.3f} GHz</text>'
            )

    conn_lines = _build_adjacency_lines(coords, edges)
    conn_html = "".join(
        f'<div class="conn-row">{html.escape(line)}</div>' for line in conn_lines
    )

    title = f"Grid Array — {n}-Transmon Chip"
    subtitle = (
        f"Designed {n}-qubit chip · TransmonPocket + RouteMeander + LaunchpadWirebond · "
        f"{len(pairs)} topology bonds · meander readout to bond pads"
    )

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"/>
<style>
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:#050810; font-family:Segoe UI,sans-serif; }}
  .wrap {{ display:flex; gap:12px; padding:10px; }}
  .chip-col {{ flex:1.35; min-width:0; }}
  .conn-col {{
    flex:0.85; background:rgba(10,22,40,0.9); border:1px solid #2a5070;
    border-radius:10px; padding:12px; max-height:580px; overflow-y:auto;
  }}
  .hdr {{ color:#9ecae8; font-size:13px; margin-bottom:4px; }}
  .sub {{ color:#5a8098; font-size:10px; margin-bottom:8px; font-family:monospace; line-height:1.4; }}
  .conn-title {{
    color:#5ecfff; font-size:10px; letter-spacing:0.15em; margin-bottom:10px;
    font-family:monospace;
  }}
  .conn-row {{
    font-size:11px; color:#9ad4ff; padding:6px 8px; margin-bottom:5px;
    border-left:2px solid #3a80b0; background:rgba(0,30,60,0.35); border-radius:4px;
    font-family:monospace;
  }}
  svg {{ width:100%; height:auto; display:block; border-radius:8px; border:1px solid #2a5070; }}
</style></head><body>
  <div class="hdr">{html.escape(title)}
    <span style="float:right;font-size:9px;border:1px solid #3a6080;padding:2px 8px;border-radius:8px;color:#6ecfff">Qiskit Metal</span>
  </div>
  <div class="sub">{html.escape(subtitle)}</div>
  <div class="wrap">
    <div class="chip-col">
      <svg viewBox="0 0 {chip_w} {chip_h}" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <filter id="glow"><feGaussianBlur stdDeviation="2"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          <filter id="boxGlow"><feGaussianBlur stdDeviation="2.5"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <rect width="{chip_w}" height="{chip_h}" fill="#030608"/>
        <rect x="45" y="45" width="{chip_w-90}" height="{chip_h-90}" rx="12" fill="#040a10" stroke="#2a6898"/>
        <text x="{chip_w/2:.0f}" y="62" fill="#4a7898" font-size="8" text-anchor="middle" font-family="monospace">Fabricated Superconducting Chip (Qiskit Metal)</text>
        {''.join(readout_lines)}
        {''.join(coupler_lines)}
        {''.join(launch_svgs)}
        {''.join(qubit_svgs)}
      </svg>
    </div>
    <div class="conn-col">
      <div class="conn-title">◈ QUBIT CONNECTIVITY MAP</div>
      {conn_html}
    </div>
  </div>
</body></html>"""
