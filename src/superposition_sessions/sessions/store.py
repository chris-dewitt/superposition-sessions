"""Persist collapsed sessions — diary, not exports folder."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def sessions_dir() -> Path:
    path = Path(os.getenv("SESSIONS_DIR", PROJECT_ROOT / "sessions"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def _poetic_timestamp(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        local = dt.astimezone()
        hour = local.hour
        if hour < 5:
            mood = "before dawn"
        elif hour < 12:
            mood = "morning collapse"
        elif hour < 17:
            mood = "afternoon measure"
        elif hour < 21:
            mood = "evening collapse"
        else:
            mood = "midnight measure"
        return f"{local.strftime('%b %d')} · {local.strftime('%I:%M %p').lstrip('0').lower()} · {mood}"
    except ValueError:
        return iso


def save_collapsed_session(record: dict[str, Any]) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    session_id = f"{now.strftime('%Y%m%d-%H%M%S')}-{record['seed_hash']}"
    record = {
        **record,
        "id": session_id,
        "collapsed_at": now.isoformat(),
        "poetic_time": _poetic_timestamp(now.isoformat()),
    }

    path = sessions_dir() / f"{session_id}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return {"id": session_id, "path": str(path)}


def list_sessions(limit: int = 50) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(sessions_dir().glob("*.json"), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            entries.append(
                {
                    "id": data.get("id", path.stem),
                    "title": data.get("vignette", {}).get("title", "untitled collapse"),
                    "poetic_time": data.get("poetic_time", _poetic_timestamp(data.get("collapsed_at", ""))),
                    "winner": data.get("winner"),
                    "seed_hash": data.get("seed_hash"),
                    "collapsed_at": data.get("collapsed_at"),
                }
            )
        except (json.JSONDecodeError, OSError):
            continue
        if len(entries) >= limit:
            break
    return entries


def load_session(session_id: str) -> dict[str, Any] | None:
    path = sessions_dir() / f"{session_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
