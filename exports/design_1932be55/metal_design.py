# AI-Driven Topo-Architect — Qiskit Metal export
# Design: design_1932be55

from qiskit_metal import designs
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket

design = designs.DesignPlanar({}, overwrite_enabled=True)
design.chips.main.size['size_x'] = '12.0mm'
design.chips.main.size['size_y'] = '8.0mm'

# Qubits
q1 = TransmonPocket(design, 'Q1', options=dict(
    pos_x='450.6um',
    pos_y='-4394.8um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q2 = TransmonPocket(design, 'Q2', options=dict(
    pos_x='-1001.1um',
    pos_y='-2179.8um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q3 = TransmonPocket(design, 'Q3', options=dict(
    pos_x='-317.1um',
    pos_y='606.6um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q4 = TransmonPocket(design, 'Q4', options=dict(
    pos_x='-23.8um',
    pos_y='3212.9um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q5 = TransmonPocket(design, 'Q5', options=dict(
    pos_x='1081.7um',
    pos_y='5508.4um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q6 = TransmonPocket(design, 'Q6', options=dict(
    pos_x='205.4um',
    pos_y='7833.3um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q7 = TransmonPocket(design, 'Q7', options=dict(
    pos_x='-579.1um',
    pos_y='10109.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q8 = TransmonPocket(design, 'Q8', options=dict(
    pos_x='-1322.8um',
    pos_y='12354.7um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q9 = TransmonPocket(design, 'Q9', options=dict(
    pos_x='-2038.6um',
    pos_y='14555.0um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q10 = TransmonPocket(design, 'Q10', options=dict(
    pos_x='3181.8um',
    pos_y='-4329.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q11 = TransmonPocket(design, 'Q11', options=dict(
    pos_x='3981.1um',
    pos_y='-1773.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q12 = TransmonPocket(design, 'Q12', options=dict(
    pos_x='2598.2um',
    pos_y='560.6um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q13 = TransmonPocket(design, 'Q13', options=dict(
    pos_x='3891.8um',
    pos_y='2670.5um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q14 = TransmonPocket(design, 'Q14', options=dict(
    pos_x='3533.0um',
    pos_y='5074.1um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q15 = TransmonPocket(design, 'Q15', options=dict(
    pos_x='5498.6um',
    pos_y='6413.4um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q16 = TransmonPocket(design, 'Q16', options=dict(
    pos_x='-1858.6um',
    pos_y='-4417.5um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q17 = TransmonPocket(design, 'Q17', options=dict(
    pos_x='1906.0um',
    pos_y='-2958.7um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q18 = TransmonPocket(design, 'Q18', options=dict(
    pos_x='-2512.0um',
    pos_y='-483.2um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q19 = TransmonPocket(design, 'Q19', options=dict(
    pos_x='-2066.3um',
    pos_y='2313.6um',
    pad_width='400um',
    pad_height='300um',
    pad_gap='30um',
    layer='1',
))

q20 = TransmonPocket(design, 'Q20', options=dict(
    pos_x='1141.2um',
    pos_y='-879.2um',
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