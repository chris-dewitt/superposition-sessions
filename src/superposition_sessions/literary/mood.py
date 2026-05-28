"""Map musical parameters to literary mood labels."""

from __future__ import annotations

from superposition_sessions.quantum.seed import SCALES, LayerParams

SCALE_NAMES = {
    0: "minor, slow — grief and almost-recognition",
    1: "dorian, drifting — wrong timeline déjà vu",
    2: "phrygian, tense — paranoia and heat",
    3: "major collapsing into doubt — bittersweet relief",
    4: "melodic minor — chosen path, loss of alternatives",
    5: "lydian, luminous — uncanny beauty",
    6: "locrian, unstable — something is off about the room",
}


def layer_mood(layer: LayerParams) -> str:
    scale_name = SCALE_NAMES.get(layer.scale_id, "unknown key")
    tempo_feel = "slow" if layer.tempo_bpm < 72 else "mid" if layer.tempo_bpm < 82 else "restless"
    return f"{layer.root} {scale_name}; tempo {tempo_feel}; voice {layer.layer_id}"
