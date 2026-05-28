"""Local Ollama vignette generation with curated fallbacks."""

from __future__ import annotations

import os
import re
from pathlib import Path

import httpx

PROMPTS_DIR = Path(__file__).resolve().parents[3] / "prompts"

FALLBACKS = [
    {
        "title": "you scrolled past your own funeral again",
        "body": (
            "the notification said someone who looked like you stopped breathing. "
            "you meant to click. you didn't. the song that's left sounds like "
            "an apology you never sent."
        ),
    },
    {
        "title": "three alarms, none of them real",
        "body": (
            "your phone knows you're still listening. it waits. the melody that "
            "survived is the one you'd hum if the building caught fire and you "
            "couldn't find the stairs."
        ),
    },
    {
        "title": "the other two are still playing somewhere",
        "body": (
            "you can't hear them anymore. that doesn't mean they stopped. "
            "somewhere a parallel tab is still open, still loading, still you."
        ),
    },
    {
        "title": "measurement completed at 3:14 am",
        "body": (
            "you collapsed the song on purpose. the universe didn't argue. "
            "what remains is the version that wanted to be found."
        ),
    },
]


def _load_prompt_template() -> str:
    path = PROMPTS_DIR / "vignette.txt"
    return path.read_text(encoding="utf-8")


def _parse_vignette(raw: str) -> dict[str, str] | None:
    title_match = re.search(r"TITLE:\s*(.+)", raw, re.IGNORECASE)
    body_match = re.search(r"BODY:\s*(.+)", raw, re.IGNORECASE | re.DOTALL)
    if not title_match or not body_match:
        return None
    title = title_match.group(1).strip().strip('"').lower()
    body = body_match.group(1).strip()
    body = re.split(r"\n\s*\n", body)[0].strip()
    if not title or not body:
        return None
    return {"title": title, "body": body}


def fallback_vignette(seed_hash: str) -> dict[str, str]:
    idx = sum(ord(c) for c in seed_hash) % len(FALLBACKS)
    return FALLBACKS[idx]


async def generate_vignette(
    seed_hash: str,
    mood: str,
    lost_count: int,
    winner: str,
) -> dict[str, str | bool]:
    prompt = _load_prompt_template().format(
        seed_hash=seed_hash,
        mood=mood,
        lost_count=lost_count,
        winner=winner,
    )

    host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.2")

    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                f"{host}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            raw = response.json().get("response", "")
            parsed = _parse_vignette(raw)
            if parsed:
                return {**parsed, "generated": True, "source": "ollama"}
    except (httpx.HTTPError, OSError):
        pass

    fb = fallback_vignette(seed_hash)
    return {**fb, "generated": False, "source": "fallback"}
