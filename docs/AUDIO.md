# Audio Design

How superposition sounds — and how collapse feels in your chest.

---

## Layer architecture

Each session generates **3 layers** (A, B, C) from one quantum seed:

| Layer | Derived from | Character |
|-------|--------------|-----------|
| A | qubit 0 measurement bias | Melodic lead — sparse |
| B | qubit 1 measurement bias | Harmonic bed — sustained |
| C | qubit 2 measurement bias | Ghost voice — detuned duplicate of A or B |

All three play simultaneously during superposition.

---

## Parameter mapping (v1)

From quantum counts → musical params:

| Quantum output | Music param | Range |
|----------------|-------------|-------|
| Bitstring prefix | Scale (minor, dorian, phrygian...) | 7 modes |
| Hamming weight | Note density | 2–8 notes/bar |
| Dominant state probability | Tempo | 60–90 BPM |
| Entropy of counts | Detune amount | 5–15 cents |

---

## Superposition mix

- Layers at equal volume initially
- Detune: layer B +8 cents, layer C -12 cents (beating)
- Reverb send: 30% on all layers (shared "room")
- No drums in v1 — space is the rhythm

---

## Collapse audio event

1. **T+0ms:** All layers play
2. **T+0ms (measure click):** 400ms silence (high-pass sweep 200Hz→8kHz on tail)
3. **T+400ms:** Survivor fades to 100%, others to 0% over 1200ms
4. **T+1600ms:** Survivor dry — reverb decays naturally

Use Web Audio API `GainNode` for fades. No jarring cuts.

---

## MIDI → audio (v1)

Week 1 path of least resistance:
- `midiutil` to generate `.mid`
- `fluidsynth` or Python `pyfluidsynth` with a soft soundfont
- Or: pure Web Audio oscillators triggered from note events (lighter, more control)

Week 4+: consider `pedalboard` or rendered WAV for canon export.

---

## Soundfont mood

Pick one soundfont for v1 and stick with it. Suggestions:
- **GeneralUser GS** — soft piano / synth pads
- Or pure sine/triangle oscillators — more abstract, more art

The instrument should sound **lonely**, not **orchestral**.

---

## Reference tracks

Listen before coding:
- Boards of Canada — *Music Has the Right to Children* (texture, nostalgia)
- Blade Runner 2049 score — "Wallace" / "Tears in the Rain" evolutions (space)
- Grouper — *Ruins* (intimacy, decay)
- Aphex Twin — *Selected Ambient Works* (beauty without crowd-pleasing)
