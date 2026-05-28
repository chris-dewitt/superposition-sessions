"""Quantum measurement → collapse one layer into classical reality."""

from __future__ import annotations

from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from superposition_sessions.quantum.seed import LayerParams

LAYER_IDS = ("A", "B", "C")
LAYER_INDEX = {"A": 0, "B": 1, "C": 2}


@dataclass(frozen=True)
class CollapseResult:
    winner: str
    losers: tuple[str, ...]
    measured_bitstring: str
    scores: dict[str, float]
    observer_bias: str | None


def collapse_session(
    seed: int,
    layers: tuple[LayerParams, LayerParams, LayerParams],
    preferred_layer: str | None = None,
) -> CollapseResult:
    """Measure the 3-qubit system; amplitude bias + observer preference pick the survivor."""
    qc = QuantumCircuit(3, 3)

    if preferred_layer and preferred_layer in LAYER_INDEX:
        qc.ry(1.15, LAYER_INDEX[preferred_layer])

    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    simulator = AerSimulator()
    collapse_seed = (seed * 7919 + 104729) & 0xFFFFFFFF
    job = simulator.run(qc, shots=1, seed_simulator=collapse_seed)
    bitstring = next(iter(job.result().get_counts()))

    scores: dict[str, float] = {}
    for layer in layers:
        idx = LAYER_INDEX[layer.layer_id]
        measured_bit = int(bitstring[2 - idx])
        observer_boost = 0.35 if layer.layer_id == preferred_layer else 0.0
        scores[layer.layer_id] = round(measured_bit + layer.amplitude_bias + observer_boost, 4)

    winner = max(scores, key=scores.get)
    losers = tuple(layer_id for layer_id in LAYER_IDS if layer_id != winner)

    return CollapseResult(
        winner=winner,
        losers=losers,
        measured_bitstring=bitstring,
        scores=scores,
        observer_bias=preferred_layer,
    )
