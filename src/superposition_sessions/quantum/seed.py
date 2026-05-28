"""Qiskit circuits → musical parameters for three superposed layers."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

SCALES = {
    0: [0, 2, 3, 5, 7, 8, 10],  # natural minor
    1: [0, 2, 3, 5, 7, 9, 10],  # dorian
    2: [0, 1, 3, 5, 7, 8, 10],  # phrygian
    3: [0, 2, 4, 5, 7, 9, 11],  # major
    4: [0, 2, 3, 5, 7, 9, 11],  # melodic minor
    5: [0, 2, 4, 6, 7, 9, 11],  # lydian
    6: [0, 2, 3, 5, 6, 8, 10],  # locrian-ish
}

ROOTS = ["C", "D", "Eb", "F", "G", "Ab", "Bb"]
ROOT_MIDI = {"C": 48, "D": 50, "Eb": 51, "F": 53, "G": 55, "Ab": 56, "Bb": 58}


@dataclass(frozen=True)
class LayerParams:
    layer_id: str
    root: str
    scale_id: int
    tempo_bpm: float
    detune_cents: float
    density: int
    amplitude_bias: float


@dataclass(frozen=True)
class SessionSeed:
    seed: int
    seed_hash: str
    counts: dict[str, int]
    layers: tuple[LayerParams, LayerParams, LayerParams]
    psi_label: str


def _run_circuit(seed: int, shots: int = 1024) -> dict[str, int]:
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots, seed_simulator=seed)
    return job.result().get_counts()


def _entropy(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    import math

    entropy = 0.0
    for value in counts.values():
        p = value / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def _layer_from_bits(layer_index: int, counts: dict[str, int]) -> LayerParams:
    total = sum(counts.values()) or 1
    weighted = 0.0
    for bitstring, count in counts.items():
        bit = bitstring[2 - layer_index]  # q2 q1 q0
        weighted += int(bit) * (count / total)

    scale_id = int(weighted * 6.999)
    root = ROOTS[(layer_index * 2 + scale_id) % len(ROOTS)]
    tempo_bpm = 60 + weighted * 30
    detune_cents = [-12, 0, 8][layer_index]
    density = 2 + int(weighted * 5.999)
    layer_names = ("A", "B", "C")

    return LayerParams(
        layer_id=layer_names[layer_index],
        root=root,
        scale_id=scale_id,
        tempo_bpm=round(tempo_bpm, 1),
        detune_cents=float(detune_cents),
        density=density,
        amplitude_bias=round(weighted, 3),
    )


def _psi_label(counts: dict[str, int]) -> str:
    total = sum(counts.values()) or 1
    amps = []
    for name in ("A", "B", "C"):
        idx = {"A": 0, "B": 1, "C": 2}[name]
        weighted = sum(
            int(bs[2 - idx]) * (c / total) for bs, c in counts.items()
        )
        amps.append(f"{weighted:.2f}|{name}⟩")
    return "|ψ⟩ = " + " + ".join(amps)


def generate_session(seed: int, shots: int = 1024) -> SessionSeed:
    counts = _run_circuit(seed, shots=shots)
    seed_hash = hashlib.sha256(f"{seed}:{counts}".encode()).hexdigest()[:12]
    layers = tuple(_layer_from_bits(i, counts) for i in range(3))
    return SessionSeed(
        seed=seed,
        seed_hash=seed_hash,
        counts=counts,
        layers=layers,  # type: ignore[arg-type]
        psi_label=_psi_label(counts),
    )
