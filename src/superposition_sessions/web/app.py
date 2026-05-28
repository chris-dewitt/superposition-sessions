"""FastAPI application — art-forward superposition session room."""

from __future__ import annotations

import os
import random
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from superposition_sessions.audio.notes import layer_to_events
from superposition_sessions.literary.mood import layer_mood
from superposition_sessions.literary.ollama import generate_vignette
from superposition_sessions.quantum.collapse import collapse_session
from superposition_sessions.quantum.seed import generate_session
from superposition_sessions.sessions.store import list_sessions, load_session, save_collapsed_session

load_dotenv()

WEB_DIR = Path(__file__).parent
STATIC_DIR = WEB_DIR / "static"
TEMPLATES = Jinja2Templates(directory=str(WEB_DIR / "templates"))

app = FastAPI(title="Superposition Sessions", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class CollapseRequest(BaseModel):
    seed: int
    seed_hash: str
    psi_label: str
    counts: dict[str, int]
    layers: list[dict[str, Any]]
    preferred_layer: str | None = None


def _session_payload(session, layers_events: list[dict]) -> dict:
    return {
        "seed": session.seed,
        "seed_hash": session.seed_hash,
        "psi_label": session.psi_label,
        "counts": session.counts,
        "layers": layers_events,
        "layer_params": [asdict(layer) for layer in session.layers],
        "created_at": time.time(),
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return TEMPLATES.TemplateResponse(
        request,
        "index.html",
        {"boot_ms": int(os.getenv("BOOT_MS", "900"))},
    )


@app.get("/api/session/new")
async def new_session(
    seed: int | None = Query(default=None),
    shots: int = Query(default=int(os.getenv("QISKIT_SHOTS", "1024"))),
) -> dict:
    session_seed = seed if seed is not None else random.randint(0, 2**31 - 1)
    session = generate_session(session_seed, shots=shots)
    layers = [layer_to_events(layer) for layer in session.layers]
    return _session_payload(session, layers)


@app.post("/api/session/collapse")
async def collapse(body: CollapseRequest) -> dict:
    session = generate_session(body.seed)
    if session.seed_hash != body.seed_hash:
        raise HTTPException(status_code=400, detail="Seed hash mismatch — session drifted.")

    if body.preferred_layer and body.preferred_layer not in {"A", "B", "C"}:
        raise HTTPException(status_code=400, detail="Observer bias must be layer A, B, or C.")

    collapse_result = collapse_session(
        seed=body.seed,
        layers=session.layers,
        preferred_layer=body.preferred_layer,
    )

    winner_params = next(
        layer for layer in session.layers if layer.layer_id == collapse_result.winner
    )
    winner_events = layer_to_events(winner_params)
    mood = layer_mood(winner_params)

    vignette = await generate_vignette(
        seed_hash=body.seed_hash,
        mood=mood,
        lost_count=len(collapse_result.losers),
        winner=collapse_result.winner,
    )

    record = {
        "seed": body.seed,
        "seed_hash": body.seed_hash,
        "psi_label_before": body.psi_label,
        "counts": body.counts,
        "winner": collapse_result.winner,
        "losers": list(collapse_result.losers),
        "measured_bitstring": collapse_result.measured_bitstring,
        "collapse_scores": collapse_result.scores,
        "observer_bias": collapse_result.observer_bias,
        "mood": mood,
        "vignette": {"title": vignette["title"], "body": vignette["body"]},
        "vignette_source": vignette.get("source", "unknown"),
        "winning_layer": winner_events,
        "all_layers": body.layers,
    }

    saved = save_collapsed_session(record)

    return {
        "winner": collapse_result.winner,
        "losers": list(collapse_result.losers),
        "measured_bitstring": collapse_result.measured_bitstring,
        "scores": collapse_result.scores,
        "psi_label_after": f"|ψ⟩ → |{collapse_result.winner}⟩",
        "vignette": {
            "title": vignette["title"],
            "body": vignette["body"],
            "generated": vignette.get("generated", False),
            "source": vignette.get("source"),
        },
        "winning_layer": winner_events,
        "saved": saved,
    }


@app.get("/api/sessions")
async def sessions(limit: int = Query(default=50, ge=1, le=200)) -> dict:
    return {"sessions": list_sessions(limit=limit)}


@app.get("/api/sessions/{session_id}")
async def session_detail(session_id: str) -> dict:
    data = load_session(session_id)
    if data is None:
        raise HTTPException(status_code=404, detail="That collapse was lost to the void.")
    return data


def create_app() -> FastAPI:
    return app
