# Roadmap — Superposition Sessions

Grow over weeks. Each week ships something you can *feel*, not just check off.

---

## Week 1 — *The room exists* ✓

**Goal:** Run one command → hear three overlapping quantum-generated loops.

| Task | Done when |
|------|-----------|
| Qiskit circuit → musical parameters (scale, tempo, note density) | ✓ `quantum/seed.py` |
| Sine-wave loop generator from seed | ✓ Web Audio, 8-bar loops per layer |
| Basic FastAPI server serves a dark single-page UI | ✓ void, orbs, listen/stop |
| Web Audio playback of 3 layers | ✓ simultaneous detuned sine waves |
| `README` quick start works on fresh clone | ✓ |

**Not in scope:** LLM, collapse, save. Just superposition you can hear.

---

## Week 2 — *Measure*

**Goal:** Collapse superposition into one saved session. It feels like an event.

| Task | Done when |
|------|-----------|
| Collapse mechanic (pick or random weighted by amplitude) | One layer survives, others fade |
| Amber collapse animation + audio crossfade | Matches DESIGN.md timing |
| Ollama integration — vignette on collapse | Title appears after measure |
| Save to `sessions/` (JSON metadata + MIDI + vignette text) | Folder grows like a diary |
| Session gallery — browse collapsed past | Minimal list, poetic timestamps |

---

## Week 3 — *Entangled duets*

**Goal:** Two layers linked by quantum entanglement — mirror/invert behavior.

| Task | Done when |
|------|-----------|
| Bell state circuit drives entangled note pairs | Changing A affects B |
| Visual link between entangled orbs (ghost magenta thread) | See the connection |
| LLM writes *pair* vignettes — two lines that reference each other | Literary entanglement |
| Optional: soft percussion from measurement clicks | Still sparse, still art |

---

## Week 4 — *The canon*

**Goal:** Your collapsed sessions become a body of work.

| Task | Done when |
|------|-----------|
| Export collapsed session as WAV | Shareable artifact |
| "Canon" view — all collapsed sessions as one scroll | Reads like a book of fragments |
| Quantum seed reproducibility — reload any session's exact superposition | Same circuit → same ghosts |
| Polish pass on DESIGN.md compliance | Typography, grain, copy audit |

---

## Week 5+ — *Wherever the multiverse goes*

Ideas backlog (pick what excites you):

- [ ] Live microphone input entangled with generated layer
- [ ] "Observer effect" — listening too long biases collapse probability
- [ ] Collaborative sessions — two users, shared entangled state
- [ ] Vinyl crackle mode
- [ ] Print vignette + QR to session

---

## Agent handoff notes

When picking up this repo:

1. Check the latest week checkbox above
2. Read `DESIGN.md` before any UI work
3. Quantum code must use Qiskit simulators — see `docs/QUANTUM.md`
4. LLM prompts live in `prompts/` — never inline giant prompts in Python
5. If Week N isn't done, don't start Week N+1 features
