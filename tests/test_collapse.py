"""Tests for quantum collapse."""

from superposition_sessions.quantum.collapse import collapse_session
from superposition_sessions.quantum.seed import generate_session


def test_collapse_picks_one_winner():
    session = generate_session(42)
    result = collapse_session(42, session.layers)
    assert result.winner in {"A", "B", "C"}
    assert len(result.losers) == 2
    assert result.winner not in result.losers


def test_collapse_reproducible():
    session = generate_session(99)
    a = collapse_session(99, session.layers)
    b = collapse_session(99, session.layers)
    assert a.winner == b.winner
    assert a.measured_bitstring == b.measured_bitstring


def test_observer_bias_can_shift_winner():
    session = generate_session(7)
    without = collapse_session(7, session.layers, preferred_layer=None)
    with_a = collapse_session(7, session.layers, preferred_layer="A")
    assert without.observer_bias is None
    assert with_a.observer_bias == "A"
