# AI-Driven Topo-Architect — Qiskit Metal export
# Design: design_dd032720

from qiskit_metal import designs
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket

design = designs.DesignPlanar({}, overwrite_enabled=True)
design.chips.main.size['size_x'] = '12.0mm'
design.chips.main.size['size_y'] = '8.0mm'

# Qubits
q1 = TransmonPocket(design, 'Q1', options=dict(
    pos_x='1781.2um',
    pos_y='-2045.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q2 = TransmonPocket(design, 'Q2', options=dict(
    pos_x='713.0um',
    pos_y='196.9um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q3 = TransmonPocket(design, 'Q3', options=dict(
    pos_x='-232.2um',
    pos_y='2453.8um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q4 = TransmonPocket(design, 'Q4', options=dict(
    pos_x='-653.7um',
    pos_y='4835.4um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q5 = TransmonPocket(design, 'Q5', options=dict(
    pos_x='-1143.8um',
    pos_y='7159.3um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q6 = TransmonPocket(design, 'Q6', options=dict(
    pos_x='-1648.9um',
    pos_y='9455.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q7 = TransmonPocket(design, 'Q7', options=dict(
    pos_x='-2150.1um',
    pos_y='11708.3um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q8 = TransmonPocket(design, 'Q8', options=dict(
    pos_x='3050.6um',
    pos_y='-4104.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q9 = TransmonPocket(design, 'Q9', options=dict(
    pos_x='4738.1um',
    pos_y='-5734.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q10 = TransmonPocket(design, 'Q10', options=dict(
    pos_x='3009.5um',
    pos_y='-89.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q11 = TransmonPocket(design, 'Q11', options=dict(
    pos_x='784.6um',
    pos_y='-4165.3um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q12 = TransmonPocket(design, 'Q12', options=dict(
    pos_x='-1581.3um',
    pos_y='616.6um',
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