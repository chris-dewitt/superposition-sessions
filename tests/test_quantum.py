"""Tests for quantum seed generation."""

from superposition_sessions.quantum.seed import generate_session


def test_generate_session_reproducible():
    a = generate_session(42)
    b = generate_session(42)
    assert a.counts == b.counts
    assert a.seed_hash == b.seed_hash
    assert len(a.layers) == 3


def test_layers_have_distinct_ids():
    session = generate_session(7)
    ids = {layer.layer_id for layer in session.layers}
    assert ids == {"A", "B", "C"}


def test_psi_label_format():
    session = generate_session(99)
    assert session.psi_label.startswith("|ψ⟩ =")
