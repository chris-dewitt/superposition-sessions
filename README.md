# Superposition Sessions

**Hold multiple songs at once. Collapse one into memory.**

A local-first quantum music instrument that generates layered musical possibilities from real qubit circuits, pairs them with sci-fi vignette fragments, and lets you *measure* — collapsing superposition into a single saved session.

Not a DAW. Not a chatbot. A ritual.

```
┌─────────────────────────────────────────────────────────┐
│  ◉  SUPERPOSITION          [ three voices, one truth ]  │
│                                                         │
│     ∿∿∿  ghost melody A    ────┐                        │
│     ∿∿∿  ghost melody B    ────┼── still uncollapsed   │
│     ∿∿∿  ghost melody C    ────┘                        │
│                                                         │
│              [ ◈ MEASURE ]                              │
│                                                         │
│  "you scrolled past your own funeral again"             │
└─────────────────────────────────────────────────────────┘
```

---

## What this is

| Layer | Role |
|-------|------|
| **Quantum (Qiskit)** | Generates musical DNA — rhythm, scale, entangled note pairs, collapse events |
| **Audio engine** | Renders 2–3 overlapping MIDI loops = superposition you can hear |
| **Local LLM (Ollama)** | Writes vignette titles, poem shards, liner notes in a curated literary voice |
| **UI** | Custom web interface — dark, slow, beautiful. Not Streamlit. Not corporate. |

---

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running
- A pair of headphones (seriously)

### Pull the local model

```bash
ollama pull llama3.2
```

---

## Quick start

```bash
git clone https://github.com/chris-dewitt/superposition-sessions.git
cd superposition-sessions
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -e .
copy .env.example .env

# Start the session room
python -m superposition_sessions
```

Open **http://127.0.0.1:7841** — click **listen**, hover orbs to solo a voice, hit **◈ measure** to collapse, browse **collapsed canon**.

**Week 2 ships:** quantum collapse, amber ritual, Ollama vignettes (with fallbacks), saved sessions.

### Ollama (optional but recommended)

```bash
ollama pull llama3.2
ollama serve
```

If Ollama isn't running, curated fallback vignettes still appear — the room never goes truly silent.

---

## Project docs

| Doc | Purpose |
|-----|---------|
| [DESIGN.md](./DESIGN.md) | Art bible — look, read, sound, feel |
| [ROADMAP.md](./ROADMAP.md) | Week-by-week build plan |
| [docs/QUANTUM.md](./docs/QUANTUM.md) | Quantum concepts used in this project |
| [docs/VOICE.md](./docs/VOICE.md) | Literary voice guide for vignettes |
| [docs/AUDIO.md](./docs/AUDIO.md) | Sound design philosophy |

---

## Repo structure (planned)

```
superposition-sessions/
├── src/superposition_sessions/
│   ├── quantum/          # Qiskit circuits → musical parameters
│   ├── audio/            # MIDI generation, layering, collapse
│   ├── literary/         # Ollama prompts, vignette generation
│   └── web/              # FastAPI + art-forward frontend
├── sessions/             # Collapsed session exports (gitignored by default)
├── prompts/              # Curated LLM prompt templates
├── static/               # Fonts, grain overlays, audio assets
└── tests/
```

---

## Working with agents

This repo is designed for multi-agent collaboration (Cursor, Claude Code, Codex).

**Before coding a feature:**
1. Read `DESIGN.md` — aesthetics are not optional
2. Check `ROADMAP.md` for the current week scope
3. Quantum logic lives in `quantum/` — don't fake it with `random.randint`

**Branch naming:** `week-1/quantum-seeds`, `week-2/collapse-ui`, etc.

---

## Philosophy

- **Real quantum.** Simulators count. Qiskit on your machine, free forever.
- **Local AI.** Your vignettes stay on your machine.
- **Art first.** If it looks like a dashboard, delete it and start over.
- **No finance. No homework.** This is for the boys.

---

## License

MIT — make weird music with it.
