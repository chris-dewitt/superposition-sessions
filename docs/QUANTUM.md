# Quantum Concepts — Superposition Sessions

Real quantum. Free. On your machine. No hand-waving.

---

## What we're using

| Tool | Cost | Purpose |
|------|------|---------|
| [Qiskit](https://qiskit.org/) | Free | Build and run circuits |
| `qiskit-aer` simulator | Free, local | Execute on your CPU |
| IBM Quantum (optional later) | Free tier | Real hardware if you want bragging rights |

---

## Concepts → music mapping

### Superposition

**Quantum:** A qubit is `|ψ⟩ = α|0⟩ + β|1⟩` — both states until measured.

**Music:** Three layers play at once. Each layer is a "possible song." You hear them overlaid — not mixed down, *coexisting*.

**Circuit (v1):** Hadamard gates on 3 qubits → equal superposition of 8 basis states → map each state to melodic parameters.

```
     ┌───┐
q_0: ┤ H ├  ── superposition of |0⟩ and |1⟩
     └───┘
```

### Measurement / collapse

**Quantum:** Measuring destroys superposition. You get one classical outcome.

**Music:** User clicks **◈ MEASURE**. One layer survives. The others decay. This is the song you "committed to."

**Circuit:** Run circuit, measure all qubits, use bitstring to select winning layer (or weight probabilities by amplitudes).

### Entanglement (Week 3)

**Quantum:** Two qubits in Bell state — measuring one instantly affects the other.

**Music:** Two melody layers mirror/invert. Entangled note pairs: when voice A hits C, voice B hits... the opposite in scale space.

**Circuit:**
```
q_0: ── H ── ● ──
              │
q_1: ──────── ⊕ ──
```

### Why not just `random`?

Because:
1. It's the real shit (your words)
2. Seeds are reproducible — same circuit + shots = same session
3. Amplitudes give weighted collapse — not uniform random
4. You learn quantum computing by making art

---

## v1 circuit sketch

```python
# Pseudocode — not final implementation
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_musical_seed(seed_int: int) -> dict:
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])           # superposition on 3 qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    simulator = AerSimulator()
    job = simulator.run(qc, shots=1024, seed_simulator=seed_int)
    counts = job.result().get_counts()

    # counts = {"000": 128, "101": 130, ...}
    # → map bitstrings to scale, tempo, density for 3 layers
    return parse_counts_to_music(counts)
```

---

## Resources

- [Qiskit Textbook — Hello World](https://learning.quantum.ibm.com/)
- [Monz Study Guide](https://github.com/desireevl/awesome-quantum-computing) if you want the deep end later

---

## Agent rule

Do not replace Qiskit with `random` for core seed generation. Simulators are fine. Cheating is not.
