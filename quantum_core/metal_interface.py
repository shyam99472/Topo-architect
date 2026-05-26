"""Qiskit Metal geometry script generation (optional runtime dependency)."""

from __future__ import annotations

from typing import Any


def metal_available() -> bool:
    try:
        import qiskit_metal  # noqa: F401
        return True
    except ImportError:
        return False


def _grid_positions_mm(n: int, chip_w: float = 9.0, chip_h: float = 6.0) -> list[tuple[float, float]]:
    cols = 2 if n <= 4 else min(3, max(2, int(n**0.5)))
    rows = (n + cols - 1) // cols
    positions = []
    for i in range(n):
        c, r = i % cols, i // cols
        sign_x = -1 if c == 0 else 1
        px = sign_x * (c + 0.5) * (chip_w / (cols + 0.5))
        py = chip_h / 2 - r * (chip_h / max(rows, 1))
        positions.append((px, py))
    return positions


def generate_metal_script(
    coordinates: list[dict],
    design_name: str = "topo_design",
    chip_size_mm: tuple[float, float] = (9.0, 6.0),
    edges: list[dict] | None = None,
) -> str:
    """
  Full Qiskit Metal script: TransmonPocket + RouteMeander couplers + LaunchpadWirebond.
  """
    n = len(coordinates)
    grid_pos = _grid_positions_mm(n, chip_size_mm[0], chip_size_mm[1])
    edges = edges or []

    lines = [
        "# AI-Driven Topo-Architect — Qiskit Metal fabricated chip",
        f"# Design: {design_name}",
        "",
        "from qiskit_metal import designs",
        "from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket",
        "from qiskit_metal.qlibrary.tlines.meandered_line import RouteMeander",
        "from qiskit_metal.qlibrary.tlines.straight_path import RouteStraight",
        "from qiskit_metal.qlibrary.terminations.launchpad_wb import LaunchpadWirebond",
        "",
        "design = designs.DesignPlanar({}, overwrite_enabled=True)",
        f"design.chips.main.size['size_x'] = '{chip_size_mm[0]}mm'",
        f"design.chips.main.size['size_y'] = '{chip_size_mm[1]}mm'",
        "",
        "# ── Transmon qubits (TransmonPocket) ──",
    ]

    for i, c in enumerate(coordinates):
        name = f"Q{i + 1}"
        px, py = grid_pos[i] if i < len(grid_pos) else (0, 0)
        lines += [
            f"{name.lower()} = TransmonPocket(design, '{name}', options=dict(",
            f"    pos_x='{px:.3f}mm',",
            f"    pos_y='{py:.2f}mm',",
            f"    pad_width='0.42mm',",
            f"    pad_height='0.32mm',",
            f"    pad_gap='0.030mm',",
            f"    inductor_width='0.008mm',",
            f"    connection_pads=dict(",
            f"        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),",
            f"        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),",
            f"    ),",
            f"    layer='1',",
            f"))",
            "",
        ]

    lines.append("# ── Meandered couplers (RouteMeander) ──")
    coupler_idx = 0
    for e in edges:
        u, v = str(e.get("source", "")), str(e.get("target", ""))
        # Map node id to Q index
        qu, qv = None, None
        for i, c in enumerate(coordinates):
            if str(c["id"]) == u:
                qu = i + 1
            if str(c["id"]) == v:
                qv = i + 1
        if qu is None or qv is None:
            continue
        coupler_idx += 1
        cname = f"C{coupler_idx}"
        lines += [
            f"{cname.lower()} = RouteMeander(design, '{cname}', options=dict(",
            f"    pin_inputs=dict(",
            f"        start_pin=dict(component='Q{qu}', pin='bus'),",
            f"        end_pin=dict(component='Q{qv}', pin='bus'),",
            f"    ),",
            f"    total_length='5.5mm',",
            f"    fillet='80um',",
            f"    lead=dict(start_straight='80um', end_straight='80um'),",
            f"    layer='1',",
            f"))",
            "",
        ]

    lines.append("# ── Launch pads (LaunchpadWirebond) ──")
    lp_positions = [
        ("LP1", "-4.0mm", "0mm"),
        ("LP2", "4.0mm", "0mm"),
        ("LP3", "0mm", "2.5mm"),
        ("LP4", "0mm", "-2.5mm"),
    ]
    for name, px, py in lp_positions[: max(4, min(6, n))]:
        lines += [
            f"{name.lower()} = LaunchpadWirebond(design, '{name}', options=dict(",
            f"    pos_x='{px}', pos_y='{py}', pad_width='0.12mm', pad_height='0.08mm', layer='1',",
            f"))",
            "",
        ]
        qn = (coupler_idx % n) + 1 if n else 1
        lines += [
            f"read_{name.lower()} = RouteMeander(design, 'R{name}', options=dict(",
            f"    pin_inputs=dict(",
            f"        start_pin=dict(component='Q{qn}', pin='readout'),",
            f"        end_pin=dict(component='{name}', pin='tie'),",
            f"    ),",
            f"    total_length='6.0mm', fillet='70um', layer='1',",
            f"))",
            "",
        ]

    lines += [
        "# ── Render & export ──",
        "from qiskit_metal import MetalGUI",
        "gui = MetalGUI(design)",
        "gui.rebuild()",
        "gui.autoscale()",
        "",
        "# design.renderers.gds.options['path_filename'] = 'exports/chip.gds'",
        "# design.renderers.gds.export_to_gds()",
    ]
    return "\n".join(lines)


def build_design_planar(
    coordinates: list[dict],
    export_gds_path: str | None = None,
    edges: list[dict] | None = None,
) -> dict[str, Any]:
    """Build real DesignPlanar when qiskit_metal is installed."""
    script = generate_metal_script(coordinates, edges=edges)
    if not metal_available():
        return {
            "success": False,
            "error": "qiskit_metal not installed",
            "script": script,
        }

    try:
        from qiskit_metal import designs
        from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket
        from qiskit_metal.qlibrary.tlines.meandered_line import RouteMeander
        from qiskit_metal.qlibrary.terminations.launchpad_wb import LaunchpadWirebond

        n = len(coordinates)
        grid_pos = _grid_positions_mm(n)
        design = designs.DesignPlanar({}, overwrite_enabled=True)
        design.chips.main.size["size_x"] = "9mm"
        design.chips.main.size["size_y"] = "6mm"

        names = []
        for i in range(n):
            name = f"Q{i + 1}"
            px, py = grid_pos[i]
            TransmonPocket(
                design,
                name,
                options={
                    "pos_x": f"{px:.3f}mm",
                    "pos_y": f"{py:.2f}mm",
                    "pad_width": "0.42mm",
                    "pad_height": "0.32mm",
                    "pad_gap": "0.030mm",
                    "connection_pads": {
                        "readout": dict(loc_W=1, loc_H=1, pad_width="80um", pad_height="40um"),
                        "bus": dict(loc_W=-1, loc_H=0, pad_width="60um", pad_height="30um"),
                    },
                    "layer": "1",
                },
            )
            names.append(name)

        gds_path = None
        if export_gds_path:
            try:
                design.renderers.gds.options["path_filename"] = export_gds_path
                design.renderers.gds.export_to_gds()
                gds_path = export_gds_path
            except Exception as exc:
                gds_path = f"export_failed: {exc}"

        return {
            "success": True,
            "qubit_names": names,
            "gds_path": gds_path,
            "script": script,
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "script": script}
