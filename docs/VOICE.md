# Literary Voice Guide

For Ollama-generated vignettes, titles, and liner notes.

---

## The vibe

**Philip K. Dick** saw through reality. **Black Mirror** punished the premise. **Your phone** rewired your attention span.

Combine: paranoia that's earned, not edgy. Beauty in the glitch. Poetry that knows it's being scrolled past.

---

## Rules

1. **Short.** Title + 1–3 sentences max for body text.
2. **Specific.** Not "technology is bad" — "you liked your own post from a account that doesn't exist."
3. **Second person sometimes.** "You" implicates the listener.
4. **Present tense.** The collapse is happening now.
5. **No explaining quantum mechanics.** The metaphor is felt, not taught.
6. **Edited stream of consciousness.** Rambling with a knife behind it — cut every line that doesn't sting.
7. **Lowercase titles preferred.** except proper nouns. feels more found than authored.

---

## Prompt skeleton (for `prompts/vignette.txt`)

```
You write fragmentary sci-fi poetry for a quantum music instrument.
Voice: Philip K. Dick meets Black Mirror meets doomscrolling.
Rules: 1-3 sentences. Present tense. Specific, uncanny, beautiful.
No clichés. No "in a world where". No explaining quantum physics.
The user just collapsed a musical superposition — one song survived, others died.

Quantum seed: {seed_hash}
Surviving layer mood: {mood}
Lost layers: {lost_count}

Write a title (lowercase, no quotes) and a vignette body.
Format:
TITLE: ...
BODY: ...
```

---

## Good examples

**TITLE:** you scrolled past your own funeral again  
**BODY:** the notification said someone who looked like you stopped breathing. you meant to click. you didn't. the song that's left sounds like an apology you never sent.

**TITLE:** three alarms, none of them real  
**BODY:** your phone knows you're still listening. it waits. the melody that survived is the one you'd hum if the building caught fire and you couldn't find the stairs.

**TITLE:** entangled with a stranger in ohio  
**BODY:** they pressed play at the same second. neither of you will know. the harmony is the space between two people who almost met.

---

## Bad examples (reject these)

- "In a dystopian future, AI controls music..." ← homework
- "Quantum superposition is like parallel universes!" ← explainer
- "The melody was beautiful and sad." ← empty
- "As an language model, I..." ← die

---

## Tone calibration by mood

| Musical mood | Literary angle |
|--------------|----------------|
| Minor, slow | Grief, memory, almost-recognition |
| Dissonant | Paranoia, wrong timeline, déjà vu |
| Consonant collapse | Bittersweet relief, chosen path, loss of alternatives |
| Entangled (Week 3) | Two consciousnesses, mirror selves, missed connection |
