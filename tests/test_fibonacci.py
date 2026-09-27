"""
Unit tests for Fibonacci algorithm implementation and input validation.
"""

import pytest
from core.tracer import RecursionTracer
from algorithms.fibonacci import run_fibonacci, fibonacci_recursive


def test_fibonacci_base_cases():
    tracer = RecursionTracer()
    assert run_fibonacci(0, tracer) == 0
    assert run_fibonacci(1, tracer) == 1


def test_fibonacci_multiple_values():
    tracer = RecursionTracer()
    assert run_fibonacci(2, tracer) == 1
    assert run_fibonacci(5, tracer) == 5
    assert run_fibonacci(6, tracer) == 8
    assert run_fibonacci(10, tracer) == 55


def test_fibonacci_event_generation():
    tracer = RecursionTracer()
    res = run_fibonacci(3, tracer)
    assert res == 2
    events = tracer.get_events()
    assert len(events) > 0

    # Verify event counts: fib(3) makes 5 total calls (fib(3), fib(2), fib(1), fib(0), fib(1))
    assert tracer.total_calls == 5
    # 5 calls + 5 returns = 10 events
    assert len(events) == 10


def test_fibonacci_invalid_inputs():
    tracer = RecursionTracer()
    with pytest.raises(ValueError):
        run_fibonacci(-1, tracer)
    with pytest.raises(ValueError):
        run_fibonacci(15, tracer)
    with pytest.raises(ValueError):
        run_fibonacci("invalid", tracer)  # type: ignore
