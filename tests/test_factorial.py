"""
Unit tests for Factorial algorithm.
"""

import pytest
from core.tracer import RecursionTracer
from algorithms.factorial import run_factorial


def test_factorial_base_cases():
    tracer = RecursionTracer()
    assert run_factorial(0, tracer) == 1
    assert run_factorial(1, tracer) == 1


def test_factorial_known_values():
    tracer = RecursionTracer()
    assert run_factorial(5, tracer) == 120
    assert run_factorial(7, tracer) == 5040
    assert run_factorial(10, tracer) == 3628800


def test_factorial_tracer_events():
    tracer = RecursionTracer()
    res = run_factorial(4, tracer)
    assert res == 24
    events = tracer.get_events()
    # 4 calls (4, 3, 2, 1) + 4 returns = 8 events
    assert len(events) == 8
    assert tracer.max_depth == 4


def test_factorial_invalid_input():
    tracer = RecursionTracer()
    with pytest.raises(ValueError):
        run_factorial(-5, tracer)
    with pytest.raises(ValueError):
        run_factorial(101, tracer)
