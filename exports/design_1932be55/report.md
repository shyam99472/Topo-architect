# AI-Driven Topo-Architect — Design Report

**Generated:** 2026-05-25 10:06 UTC

## User Request
> I need 20 qubits in a heavy-hex layout with frequencies between 4.6 and 5.2 GHz

## Design Summary
- **Qubits:** 20
- **Lattice:** heavy_hex
- **Nodes / Edges:** 20 / 26
- **Frequency range (GHz):** [4.5, 5.5]

## Physics Metrics
- **Connectivity score (E/V):** 1.3
- **Layout density:** 0.132
- **Crosstalk estimate:** 9.1685
- **Frequency collisions:** 13
- **Spatial crosstalk flags:** 0

## Optimization
- **Crosstalk before:** 94.2225
- **Crosstalk after:** 9.1685
- **Improvement:** 90.3%

## Validation
- **Status:** ISSUES FOUND
### Errors
- Δf=150.0 MHz < 200 MHz between q0 and q1
- Δf=150.0 MHz < 200 MHz between q1 and q2
- Δf=150.0 MHz < 200 MHz between q2 and q3
- Δf=150.0 MHz < 200 MHz between q3 and q4
- Δf=150.0 MHz < 200 MHz between q4 and q5
- Δf=150.0 MHz < 200 MHz between q5 and q6
- Δf=150.0 MHz < 200 MHz between q6 and q7
- Δf=150.0 MHz < 200 MHz between q7 and q8
- Δf=150.0 MHz < 200 MHz between q9 and q10
- Δf=150.0 MHz < 200 MHz between q10 and q11
- Δf=150.0 MHz < 200 MHz between q11 and q12
- Δf=150.0 MHz < 200 MHz between q12 and q13
- Δf=150.0 MHz < 200 MHz between q13 and q14
### Warnings
- Connectivity C=1.30 deviates from target ~3.0

## AI Analysis
_Ollama offline — report uses computed metrics only._