# AI-Driven Topo-Architect — Qiskit Metal export
# Design: design_017323bc

from qiskit_metal import designs
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket

design = designs.DesignPlanar({}, overwrite_enabled=True)
design.chips.main.size['size_x'] = '12.0mm'
design.chips.main.size['size_y'] = '8.0mm'

# Qubits
q1 = TransmonPocket(design, 'Q1', options=dict(
    pos_x='-96.4um',
    pos_y='-3977.6um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q2 = TransmonPocket(design, 'Q2', options=dict(
    pos_x='-575.9um',
    pos_y='-1485.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q3 = TransmonPocket(design, 'Q3', options=dict(
    pos_x='1059.1um',
    pos_y='618.3um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q4 = TransmonPocket(design, 'Q4', options=dict(
    pos_x='767.9um',
    pos_y='3180.9um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q5 = TransmonPocket(design, 'Q5', options=dict(
    pos_x='276.3um',
    pos_y='5592.6um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q6 = TransmonPocket(design, 'Q6', options=dict(
    pos_x='-131.1um',
    pos_y='7956.5um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q7 = TransmonPocket(design, 'Q7', options=dict(
    pos_x='-516.8um',
    pos_y='10297.7um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q8 = TransmonPocket(design, 'Q8', options=dict(
    pos_x='-892.6um',
    pos_y='12618.6um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q9 = TransmonPocket(design, 'Q9', options=dict(
    pos_x='-1259.6um',
    pos_y='14898.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q10 = TransmonPocket(design, 'Q10', options=dict(
    pos_x='2286.3um',
    pos_y='-4914.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q11 = TransmonPocket(design, 'Q11', options=dict(
    pos_x='4109.0um',
    pos_y='-3178.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q12 = TransmonPocket(design, 'Q12', options=dict(
    pos_x='3272.2um',
    pos_y='-796.3um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q13 = TransmonPocket(design, 'Q13', options=dict(
    pos_x='-2250.9um',
    pos_y='-3178.7um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q14 = TransmonPocket(design, 'Q14', options=dict(
    pos_x='1727.5um',
    pos_y='-2892.8um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q15 = TransmonPocket(design, 'Q15', options=dict(
    pos_x='-1328.2um',
    pos_y='658.3um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q16 = TransmonPocket(design, 'Q16', options=dict(
    pos_x='2803.2um',
    pos_y='2273.8um',
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