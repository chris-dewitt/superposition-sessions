# Design Bible — Superposition Sessions

> *The app should feel like finding a bootleg recording in a universe you almost lived in.*

---

## North star

Every screen must pass four tests:

1. **Look like art** — composition, negative space, intentional imperfection
2. **Read like art** — vignettes worth screenshotting, not filler
3. **Sound like art** — detuned layers, breath, decay, collapse
4. **Feel like art** — slow, ceremonial, a little unsettling

If it feels like SaaS, kill it.

---

## Visual language

### Palette

| Name | Hex | Use |
|------|-----|-----|
| Void | `#08080c` | Background — not pure black, slightly blue-dead |
| Phosphor | `#00ffd5` | Active superposition layers, quantum readouts |
| Amber Collapse | `#ffb347` | Measurement events, locked-in choices |
| Ghost | `#ff2d95` | Entangled pairs, literary accents |
| Ash | `#6b7280` | Secondary text, timestamps |
| Bone | `#e8e4dc` | Primary poetry text — warm, not sterile white |

### Typography

| Role | Font | Why |
|------|------|-----|
| Poetry / vignettes | **Instrument Serif** or **Libre Baskerville** | Literary, human, slightly haunted |
| UI labels | **DM Sans** or **Inter** (light weight only) | Quiet, never shouts |
| Quantum state | **JetBrains Mono** | Machine truth beneath the poetry |

Rules:
- Vignette text: generous line-height (1.7+), max-width ~42ch
- Never bold the poetry — let size and space do the work
- All caps only for quantum measurement readouts

### Texture & motion

- **Film grain overlay** at 3–5% opacity — static, not animated noise
- **Slow pulse** on superposition orbs (4–6 second breathe cycle)
- **Collapse animation:** layers don't snap off — they *phase out* over 1.2s with amber flash
- **No bounce easing.** No Material Design ripples. Ease-in-out or linear only.
- Optional: faint horizontal scanline CSS at 2% opacity (Blade Runner nod without cosplay)

### Layout principles

- **One focal point per screen.** Never dashboard grids.
- **Generous margins.** The void is part of the design.
- Center the poetry. Push controls to the edges or bottom — they're secondary.
- Dark mode only. There is no light mode. You are in the session room.

---

## Interaction ritual

### Entering a session

1. Screen fades from void → faint phosphor grid
2. Text: *"tuning qubits..."* (800ms minimum, even if ready faster)
3. Three orbs fade in — each a superposed voice
4. Audio layers fade up staggered (200ms apart)

### During superposition

- Hover an orb: that layer brightens, others dim to 40%
- Click orb: solo listen (others muted, not removed)
- Quantum readout (mono, small, bottom-left): `|ψ⟩ = 0.58|A⟩ + 0.61|B⟩ + 0.54|C⟩`

### Measurement (collapse)

- Button copy: **◈ MEASURE** — not "Save" or "Export"
- On click: 400ms silence → amber flash → one layer survives
- Surviving layer gets a vignette title from the LLM
- Others decay with reverb tail (audio) and opacity fade (visual)
- Session saved to `sessions/` with timestamp + quantum seed hash

### Copy tone (UI microcopy)

| ✗ Don't | ✓ Do |
|---------|------|
| "Generate new track" | "Open another session" |
| "Error: model failed" | "The room went quiet. Try again." |
| "Loading..." | "Listening for parallel selves..." |
| "Export MIDI" | "Take the collapsed recording" |

---

## Sound design

See [docs/AUDIO.md](./docs/AUDIO.md) for technical detail. Principles:

- **Superposition = detune.** Layers are ±5–15 cents apart. Close enough to beat, not enough to clash instantly.
- **Scales from quantum seeds.** Not random notes — circuit output maps to scale degrees.
- **Entangled pairs:** two voices that mirror or invert — when one rises, the other falls.
- **Collapse = high-pass sweep + silence gap.** The universe holds its breath.
- **Tempo:** 60–90 BPM. Slow. Room to think.
- **Instrumentation (v1):** soft sine/square synth, no drums until Week 3+. The void needs space.

Reference moods: Boards of Canada, early Aphex ambient, Blade Runner 2049 score (sparse), Grouper.

---

## Literary voice

See [docs/VOICE.md](./docs/VOICE.md) for full guide. Summary:

- Philip K. Dick paranoia + Black Mirror premise + Instagram brain rot
- Second person, present tense, sometimes
- Stream of consciousness but **edited** — every line earns its place
- Never explain the quantum metaphor. Let it sit.
- 1–3 sentences per vignette. Titles can be longer than bodies.

**Example vignette titles:**
- *you scrolled past your own funeral again*
- *the algorithm remembered a childhood you never had*
- *three versions of you hummed the same wrong note*

---

## Tech approach (for art, not despite it)

**Why FastAPI + custom HTML/CSS/JS (not Streamlit, not default Gradio):**
- Full control over typography, animation, Web Audio API
- Gradio is fine for prototypes — we graduate to custom by Week 2
- Week 1 may use a minimal FastAPI shell with hand-written CSS

**Frontend stack (planned):**
- FastAPI backend
- Vanilla JS + Web Audio API for layer mixing
- CSS custom properties for the palette above
- Self-hosted fonts in `static/fonts/`

---

## Anti-patterns (instant reject)

- Purple gradient backgrounds
- Card-based dashboard layouts
- "AI Music Generator 🎵" energy
- Stock icons
- Light mode
- Explaining quantum computing in tooltip paragraphs
- Generic cyberpunk (neon for neon's sake)

---

## Success criteria

You'll know it's working when:

1. You open it at midnight and lose 20 minutes without composing anything
2. A friend asks "what is this?" and you can't explain but they want to try
3. The collapsed sessions folder feels like a diary, not a exports folder
4. You read a generated vignette and feel something, not nothing
