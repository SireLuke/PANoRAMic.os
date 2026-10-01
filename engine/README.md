# Engine subsystem

The engine layer is responsible for the simulation loop, planetary updates, and system execution.

Design parameters:
- tick cadence: continuous loop
- update cycle: world state evaluation + signal recomputation
- economic engine: PAR supply, demurrage, scarcity, and resource flows
- dashboard updates: refresh state on each tick
- CLI integration: command dispatch and operational control

This subsystem ties the model layer to the runtime and operational control plane.
