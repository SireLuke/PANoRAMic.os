# Quantum Computing & Information Board

**Status:** proposal. **Purpose:** investigate quantum information and computation with explicit baselines, resource accounting, and reproducible circuit or device experiments.

## Scope

Quantum circuits, graph/stabilizer states, measurement-based computation; error correction, fault tolerance, decoding, noise; graph theory, coding and information theory, quantum complexity; simulation, hardware experiments, compilation, resource estimates; E8/Gosset-derived encodings only where a concrete encoding and measurable benefit are specified.

## Starter questions

1. Which graph families produce useful stabilizer states or code constructions under known metrics?
2. Do Gosset/E8-derived graphs offer measurable advantage over degree-, size-, and symmetry-matched baselines?
3. Can encodings reduce circuit depth, gate count, decoding complexity, or logical error rate?
4. How do noise, connectivity, compilation overhead, and finite-size effects change results?
5. Can an advantage be reproduced on independent simulators or hardware?

## Minimum controls

Compare strong classical and quantum baselines. Count qubits, gates, depth, connectivity overhead, shots, runtime, memory, and error rates. State whether results are analytic, simulated, or hardware-observed. Include noise assumptions and uncertainty. Graph resemblance alone does not establish quantum advantage.

Entry fields: problem/task; encoding/circuit/code; baseline; resource accounting; noise/hardware; result/uncertainty; reproduction artifact; interpretation boundary.

Authored-by: OpenAI (ChatGPT bench)
