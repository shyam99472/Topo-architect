# AI-Driven Topo-Architect — Qiskit Metal export
# Design: design_95424b0d

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
    pos_x='500.0um',
    pos_y='5196.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q8 = TransmonPocket(design, 'Q8', options=dict(
    pos_x='0.0um',
    pos_y='6062.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q9 = TransmonPocket(design, 'Q9', options=dict(
    pos_x='500.0um',
    pos_y='6928.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q10 = TransmonPocket(design, 'Q10', options=dict(
    pos_x='1500.0um',
    pos_y='0.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q11 = TransmonPocket(design, 'Q11', options=dict(
    pos_x='2000.0um',
    pos_y='866.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q12 = TransmonPocket(design, 'Q12', options=dict(
    pos_x='1500.0um',
    pos_y='1732.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q13 = TransmonPocket(design, 'Q13', options=dict(
    pos_x='2000.0um',
    pos_y='2598.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q14 = TransmonPocket(design, 'Q14', options=dict(
    pos_x='1500.0um',
    pos_y='3464.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q15 = TransmonPocket(design, 'Q15', options=dict(
    pos_x='2000.0um',
    pos_y='4330.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q16 = TransmonPocket(design, 'Q16', options=dict(
    pos_x='250.0um',
    pos_y='433.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q17 = TransmonPocket(design, 'Q17', options=dict(
    pos_x='1000.0um',
    pos_y='0.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q18 = TransmonPocket(design, 'Q18', options=dict(
    pos_x='250.0um',
    pos_y='1299.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q19 = TransmonPocket(design, 'Q19', options=dict(
    pos_x='250.0um',
    pos_y='2165.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q20 = TransmonPocket(design, 'Q20', options=dict(
    pos_x='1000.0um',
    pos_y='1732.1um',
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