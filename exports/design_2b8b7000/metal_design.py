# AI-Driven Topo-Architect — Qiskit Metal fabricated chip
# Design: design_2b8b7000

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
    pos_x='-1.800mm',
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
    pos_x='5.400mm',
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
    pos_x='-1.800mm',
    pos_y='1.50mm',
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
    pos_x='5.400mm',
    pos_y='1.50mm',
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
    pos_x='-1.800mm',
    pos_y='0.00mm',
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
    pos_x='5.400mm',
    pos_y='0.00mm',
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
    pos_x='-1.800mm',
    pos_y='-1.50mm',
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
        end_pin=dict(component='Q7', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c3 = RouteMeander(design, 'C3', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q2', pin='bus'),
        end_pin=dict(component='Q3', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c4 = RouteMeander(design, 'C4', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q2', pin='bus'),
        end_pin=dict(component='Q7', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c5 = RouteMeander(design, 'C5', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q3', pin='bus'),
        end_pin=dict(component='Q4', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c6 = RouteMeander(design, 'C6', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q4', pin='bus'),
        end_pin=dict(component='Q5', pin='bus'),
    ),
    total_length='5.5mm',
    fillet='80um',
    lead=dict(start_straight='80um', end_straight='80um'),
    layer='1',
))

c7 = RouteMeander(design, 'C7', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q5', pin='bus'),
        end_pin=dict(component='Q6', pin='bus'),
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
        start_pin=dict(component='Q1', pin='readout'),
        end_pin=dict(component='LP1', pin='tie'),
    ),
    total_length='6.0mm', fillet='70um', layer='1',
))

lp2 = LaunchpadWirebond(design, 'LP2', options=dict(
    pos_x='4.0mm', pos_y='0mm', pad_width='0.12mm', pad_height='0.08mm', layer='1',
))

read_lp2 = RouteMeander(design, 'RLP2', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q1', pin='readout'),
        end_pin=dict(component='LP2', pin='tie'),
    ),
    total_length='6.0mm', fillet='70um', layer='1',
))

lp3 = LaunchpadWirebond(design, 'LP3', options=dict(
    pos_x='0mm', pos_y='2.5mm', pad_width='0.12mm', pad_height='0.08mm', layer='1',
))

read_lp3 = RouteMeander(design, 'RLP3', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q1', pin='readout'),
        end_pin=dict(component='LP3', pin='tie'),
    ),
    total_length='6.0mm', fillet='70um', layer='1',
))

lp4 = LaunchpadWirebond(design, 'LP4', options=dict(
    pos_x='0mm', pos_y='-2.5mm', pad_width='0.12mm', pad_height='0.08mm', layer='1',
))

read_lp4 = RouteMeander(design, 'RLP4', options=dict(
    pin_inputs=dict(
        start_pin=dict(component='Q1', pin='readout'),
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