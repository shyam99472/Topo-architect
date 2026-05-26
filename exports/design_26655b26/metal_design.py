# AI-Driven Topo-Architect — Qiskit Metal fabricated chip
# Design: design_26655b26

from qiskit_metal import designs
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket
from qiskit_metal.qlibrary.tlines.meandered_line import RouteMeander
from qiskit_metal.qlibrary.tlines.straight_path import RouteStraight
from qiskit_metal.qlibrary.terminations.launchpad_wb import LaunchpadWirebond

design = designs.DesignPlanar({}, overwrite_enabled=True)
design.chips.main.size['size_x'] = '9.0mm'
design.chips.main.size['size_y'] = '6.0mm'

# ── Transmon qubits (TransmonPocket) ──
q1 = TransmonPocket(design, 'Q1', options=dict(
    pos_x='-1.286mm',
    pos_y='3.00mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q2 = TransmonPocket(design, 'Q2', options=dict(
    pos_x='3.857mm',
    pos_y='3.00mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q3 = TransmonPocket(design, 'Q3', options=dict(
    pos_x='6.429mm',
    pos_y='3.00mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q4 = TransmonPocket(design, 'Q4', options=dict(
    pos_x='-1.286mm',
    pos_y='2.14mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q5 = TransmonPocket(design, 'Q5', options=dict(
    pos_x='3.857mm',
    pos_y='2.14mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q6 = TransmonPocket(design, 'Q6', options=dict(
    pos_x='6.429mm',
    pos_y='2.14mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q7 = TransmonPocket(design, 'Q7', options=dict(
    pos_x='-1.286mm',
    pos_y='1.29mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q8 = TransmonPocket(design, 'Q8', options=dict(
    pos_x='3.857mm',
    pos_y='1.29mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q9 = TransmonPocket(design, 'Q9', options=dict(
    pos_x='6.429mm',
    pos_y='1.29mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q10 = TransmonPocket(design, 'Q10', options=dict(
    pos_x='-1.286mm',
    pos_y='0.43mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q11 = TransmonPocket(design, 'Q11', options=dict(
    pos_x='3.857mm',
    pos_y='0.43mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q12 = TransmonPocket(design, 'Q12', options=dict(
    pos_x='6.429mm',
    pos_y='0.43mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q13 = TransmonPocket(design, 'Q13', options=dict(
    pos_x='-1.286mm',
    pos_y='-0.43mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q14 = TransmonPocket(design, 'Q14', options=dict(
    pos_x='3.857mm',
    pos_y='-0.43mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q15 = TransmonPocket(design, 'Q15', options=dict(
    pos_x='6.429mm',
    pos_y='-0.43mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q16 = TransmonPocket(design, 'Q16', options=dict(
    pos_x='-1.286mm',
    pos_y='-1.29mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q17 = TransmonPocket(design, 'Q17', options=dict(
    pos_x='3.857mm',
    pos_y='-1.29mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q18 = TransmonPocket(design, 'Q18', options=dict(
    pos_x='6.429mm',
    pos_y='-1.29mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q19 = TransmonPocket(design, 'Q19', options=dict(
    pos_x='-1.286mm',
    pos_y='-2.14mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

q20 = TransmonPocket(design, 'Q20', options=dict(
    pos_x='3.857mm',
    pos_y='-2.14mm',
    pad_width='0.42mm',
    pad_height='0.32mm',
    pad_gap='0.030mm',
    inductor_width='0.008mm',
    connection_pads=dict(
        readout=dict(loc_W=1, loc_H=1, pad_width='80um', pad_height='40um'),
        bus=dict(loc_W=-1, loc_H=0, pad_width='60um', pad_height='30um'),
    ),
    layer='1',
))

# ── Meandered couplers (RouteMeander) ──
c1 = RouteMeander(design, 'C1', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q1', pin='bus'),
        end_pin=dict(component='Q2', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c2 = RouteMeander(design, 'C2', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q1', pin='bus'),
        end_pin=dict(component='Q10', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c3 = RouteMeander(design, 'C3', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q1', pin='bus'),
        end_pin=dict(component='Q16', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c4 = RouteMeander(design, 'C4', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q1', pin='bus'),
        end_pin=dict(component='Q17', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c5 = RouteMeander(design, 'C5', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q2', pin='bus'),
        end_pin=dict(component='Q3', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c6 = RouteMeander(design, 'C6', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q2', pin='bus'),
        end_pin=dict(component='Q16', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c7 = RouteMeander(design, 'C7', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q2', pin='bus'),
        end_pin=dict(component='Q18', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c8 = RouteMeander(design, 'C8', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q3', pin='bus'),
        end_pin=dict(component='Q4', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c9 = RouteMeander(design, 'C9', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q3', pin='bus'),
        end_pin=dict(component='Q12', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c10 = RouteMeander(design, 'C10', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q3', pin='bus'),
        end_pin=dict(component='Q18', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c11 = RouteMeander(design, 'C11', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q3', pin='bus'),
        end_pin=dict(component='Q19', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c12 = RouteMeander(design, 'C12', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q3', pin='bus'),
        end_pin=dict(component='Q20', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c13 = RouteMeander(design, 'C13', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q4', pin='bus'),
        end_pin=dict(component='Q5', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c14 = RouteMeander(design, 'C14', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q4', pin='bus'),
        end_pin=dict(component='Q19', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c15 = RouteMeander(design, 'C15', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q5', pin='bus'),
        end_pin=dict(component='Q6', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c16 = RouteMeander(design, 'C16', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q5', pin='bus'),
        end_pin=dict(component='Q14', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c17 = RouteMeander(design, 'C17', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q6', pin='bus'),
        end_pin=dict(component='Q7', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c18 = RouteMeander(design, 'C18', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q7', pin='bus'),
        end_pin=dict(component='Q8', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c19 = RouteMeander(design, 'C19', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q8', pin='bus'),
        end_pin=dict(component='Q9', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c20 = RouteMeander(design, 'C20', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q10', pin='bus'),
        end_pin=dict(component='Q11', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c21 = RouteMeander(design, 'C21', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q10', pin='bus'),
        end_pin=dict(component='Q17', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c22 = RouteMeander(design, 'C22', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q11', pin='bus'),
        end_pin=dict(component='Q12', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c23 = RouteMeander(design, 'C23', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q11', pin='bus'),
        end_pin=dict(component='Q17', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c24 = RouteMeander(design, 'C24', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q12', pin='bus'),
        end_pin=dict(component='Q13', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c25 = RouteMeander(design, 'C25', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q12', pin='bus'),
        end_pin=dict(component='Q20', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c26 = RouteMeander(design, 'C26', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q13', pin='bus'),
        end_pin=dict(component='Q14', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c27 = RouteMeander(design, 'C27', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q14', pin='bus'),
        end_pin=dict(component='Q15', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c28 = RouteMeander(design, 'C28', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q17', pin='bus'),
        end_pin=dict(component='Q20', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

# ── Launch pads (LaunchpadWirebond) ──
lp1 = LaunchpadWirebond(design, 'LP1', options=dict(
    pos_x='-4.0mm', pos_y='0mm', pad_width='0.12mm', pad_height='0.08mm', layer='1',
))

read_lp1 = RouteMeander(design, 'RLP1', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q9', pin='readout'),
        end_pin=dict(component='LP1', pin='tie'),
    ),
    total_length='6.0mm', fillet='70um', layer='1',
))

lp2 = LaunchpadWirebond(design, 'LP2', options=dict(
    pos_x='4.0mm', pos_y='0mm', pad_width='0.12mm', pad_height='0.08mm', layer='1',
))

read_lp2 = RouteMeander(design, 'RLP2', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q9', pin='readout'),
        end_pin=dict(component='LP2', pin='tie'),
    ),
    total_length='6.0mm', fillet='70um', layer='1',
))

lp3 = LaunchpadWirebond(design, 'LP3', options=dict(
    pos_x='0mm', pos_y='2.5mm', pad_width='0.12mm', pad_height='0.08mm', layer='1',
))

read_lp3 = RouteMeander(design, 'RLP3', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q9', pin='readout'),
        end_pin=dict(component='LP3', pin='tie'),
    ),
    total_length='6.0mm', fillet='70um', layer='1',
))

lp4 = LaunchpadWirebond(design, 'LP4', options=dict(
    pos_x='0mm', pos_y='-2.5mm', pad_width='0.12mm', pad_height='0.08mm', layer='1',
))

read_lp4 = RouteMeander(design, 'RLP4', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q9', pin='readout'),
        end_pin=dict(component='LP4', pin='tie'),
    ),
    total_length='6.0mm', fillet='70um', layer='1',
))

# ── Render & export ──
from qiskit_metal import MetalGUI
gui = MetalGUI(design)
gui.rebuild()
gui.autoscale()

# design.renderers.gds.options['path_filename'] = 'exports/chip.gds'
# design.renderers.gds.export_to_gds()