"""Convert layer parameters into note events for Web Audio sine synthesis."""

from __future__ import annotations

from typing import Any

from superposition_sessions.quantum.seed import ROOT_MIDI, SCALES, LayerParams


def _midi_to_freq(midi: int) -> float:
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


def layer_to_events(layer: LayerParams, bars: int = 8) -> dict[str, Any]:
    root_midi = ROOT_MIDI[layer.root]
    scale = SCALES[layer.scale_id]
    beat_duration = 60.0 / layer.tempo_bpm
    bar_duration = beat_duration * 4

    events: list[dict[str, float | str]] = []
    step = 0
    for bar in range(bars):
        for beat in range(4):
            if step % max(1, (8 // layer.density)) != 0:
                step += 1
                continue

            degree_idx = (bar * 3 + beat * 2 + int(layer.amplitude_bias * 4)) % len(
                scale
            )
            octave_shift = 12 if layer.layer_id == "B" else 0
            if layer.layer_id == "C":
                octave_shift = 24

            midi = root_midi + scale[degree_idx] + octave_shift
            start = bar * bar_duration + beat * beat_duration
            duration = beat_duration * (1.5 if layer.layer_id == "B" else 0.85)

            events.append(
                {
                    "freq": round(_midi_to_freq(midi), 3),
                    "start": round(start, 4),
                    "duration": round(duration, 4),
                    "gain": 0.18 if layer.layer_id == "B" else 0.24,
                }
            )
            step += 1

    loop_duration = bars * bar_duration
    return {
        "layer_id": layer.layer_id,
        "root": layer.root,
        "scale_id": layer.scale_id,
        "tempo_bpm": layer.tempo_bpm,
        "detune_cents": layer.detune_cents,
        "loop_duration": round(loop_duration, 4),
        "events": events,
    }
