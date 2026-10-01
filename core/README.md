# Core subsystem

The core layer defines the base PAN state and economic logic.

Key repo parameters:
- floatMultiplier: 1.35
- resourceMultiplier: 0.90
- MSRP cap: 15% of market value
- dynamic PAR cap = min(worldPopulation * floatMultiplier, resourceParValue * resourceMultiplier)
- system state tracks ecology, infrastructure, markets, modes, PAR, nodes, workforce, and dashboard metrics

This folder acts as the canonical model layer for PANoRAMic.os.
