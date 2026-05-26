# AI-Driven Topo-Architect — Qiskit Metal export
# Design: design_328d5486

from qiskit_metal import designs
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket

design = designs.DesignPlanar({}, overwrite_enabled=True)
design.chips.main.size['size_x'] = '12.0mm'
design.chips.main.size['size_y'] = '8.0mm'

# Qubits
q1 = TransmonPocket(design, 'Q1', options=dict(
    pos_x='500.0um',
    pos_y='0.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q2 = TransmonPocket(design, 'Q2', options=dict(
    pos_x='0.0um',
    pos_y='866.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q3 = TransmonPocket(design, 'Q3', options=dict(
    pos_x='500.0um',
    pos_y='1732.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q4 = TransmonPocket(design, 'Q4', options=dict(
    pos_x='0.0um',
    pos_y='2598.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q5 = TransmonPocket(design, 'Q5', options=dict(
    pos_x='500.0um',
    pos_y='3464.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q6 = TransmonPocket(design, 'Q6', options=dict(
    pos_x='0.0um',
    pos_y='4330.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q7 = TransmonPocket(design, 'Q7', options=dict(
    pos_x='250.0um',
    pos_y='433.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q8 = TransmonPocket(design, 'Q8', options=dict(
    pos_x='1000.0um',
    pos_y='0.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

# Export GDS (requires KLayout renderer)
# design.renderers.gds.options['path_filename'] = 'exports/chip.gds'
# design.renderers.gds.export_to_gds()

# from qiskit_metal import MetalGUI
# gui = MetalGUI(design)
# gui.rebuild()