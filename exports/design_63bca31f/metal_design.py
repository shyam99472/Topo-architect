# AI-Driven Topo-Architect — Qiskit Metal export
# Design: design_63bca31f

from qiskit_metal import designs
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket

design = designs.DesignPlanar({}, overwrite_enabled=True)
design.chips.main.size['size_x'] = '12.0mm'
design.chips.main.size['size_y'] = '8.0mm'

# Qubits
q1 = TransmonPocket(design, 'Q1', options=dict(
    pos_x='-11.4um',
    pos_y='-3564.5um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q2 = TransmonPocket(design, 'Q2', options=dict(
    pos_x='-559.9um',
    pos_y='-1106.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q3 = TransmonPocket(design, 'Q3', options=dict(
    pos_x='1109.6um',
    pos_y='940.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q4 = TransmonPocket(design, 'Q4', options=dict(
    pos_x='675.1um',
    pos_y='3380.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q5 = TransmonPocket(design, 'Q5', options=dict(
    pos_x='301.9um',
    pos_y='5757.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q6 = TransmonPocket(design, 'Q6', options=dict(
    pos_x='-52.3um',
    pos_y='8111.8um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q7 = TransmonPocket(design, 'Q7', options=dict(
    pos_x='-398.2um',
    pos_y='10452.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q8 = TransmonPocket(design, 'Q8', options=dict(
    pos_x='-738.9um',
    pos_y='12775.3um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q9 = TransmonPocket(design, 'Q9', options=dict(
    pos_x='-1072.5um',
    pos_y='15058.7um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q10 = TransmonPocket(design, 'Q10', options=dict(
    pos_x='2405.8um',
    pos_y='-4069.7um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q11 = TransmonPocket(design, 'Q11', options=dict(
    pos_x='4136.3um',
    pos_y='-2279.8um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q12 = TransmonPocket(design, 'Q12', options=dict(
    pos_x='3562.5um',
    pos_y='145.6um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q13 = TransmonPocket(design, 'Q13', options=dict(
    pos_x='-2206.5um',
    pos_y='-2755.7um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q14 = TransmonPocket(design, 'Q14', options=dict(
    pos_x='837.7um',
    pos_y='-5758.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q15 = TransmonPocket(design, 'Q15', options=dict(
    pos_x='1568.3um',
    pos_y='-1168.1um',
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