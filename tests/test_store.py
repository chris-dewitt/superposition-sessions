"""Tests for session persistence."""

from superposition_sessions.sessions.store import list_sessions, load_session, save_collapsed_session


def test_save_and_load_session(tmp_path, monkeypatch):
    monkeypatch.setenv("SESSIONS_DIR", str(tmp_path))

    saved = save_collapsed_session(
        {
            "seed": 42,
            "seed_hash": "abc123",
            "winner": "B",
            "vignette": {"title": "test collapse", "body": "one song survived."},
        }
    )

    loaded = load_session(saved["id"])
    assert loaded is not None
    assert loaded["winner"] == "B"
    assert loaded["vignette"]["title"] == "test collapse"
    assert "poetic_time" in loaded


def test_list_sessions_newest_first(tmp_path, monkeypatch):
    monkeypatch.setenv("SESSIONS_DIR", str(tmp_path))

    save_collapsed_session(
        {"seed": 1, "seed_hash": "aaa", "winner": "A", "vignette": {"title": "first", "body": "x"}}
    )
    save_collapsed_session(
        {"seed": 2, "seed_hash": "bbb", "winner": "C", "vignette": {"title": "second", "body": "y"}}
    )

    sessions = list_sessions()
    assert len(sessions) >= 2
    assert sessions[0]["seed_hash"] == "bbb"
