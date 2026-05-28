"""FastAPI application — art-forward superposition session room."""

from __future__ import annotations

import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from superposition_sessions.audio.notes import layer_to_events
from superposition_sessions.quantum.seed import generate_session

load_dotenv()

WEB_DIR = Path(__file__).parent
STATIC_DIR = WEB_DIR / "static"
TEMPLATES = Jinja2Templates(directory=str(WEB_DIR / "templates"))

app = FastAPI(title="Superposition Sessions", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "boot_ms": int(os.getenv("BOOT_MS", "900"))},
    )


@app.get("/api/session/new")
async def new_session(
    seed: int | None = Query(default=None),
    shots: int = Query(default=int(os.getenv("QISKIT_SHOTS", "1024"))),
) -> dict:
    session_seed = seed if seed is not None else random.randint(0, 2**31 - 1)
    session = generate_session(session_seed, shots=shots)
    layers = [layer_to_events(layer) for layer in session.layers]

    return {
        "seed": session.seed,
        "seed_hash": session.seed_hash,
        "psi_label": session.psi_label,
        "counts": session.counts,
        "layers": layers,
        "created_at": time.time(),
    }


def create_app() -> FastAPI:
    return app
