"""
Unit tests for N-Queens recursive backtracking solver.
"""

import pytest
from core.tracer import RecursionTracer
from algorithms.n_queens import run_n_queens, is_safe


def test_is_safe_check():
    # Board size 4: placing queen on row 0, col 1
    queens = [1, -1, -1, -1]
    # Row 1, col 1 -> same column attack -> unsafe
    assert not is_safe(queens, 1, 1)
    # Row 1, col 2 -> diagonal attack -> unsafe
    assert not is_safe(queens, 1, 2)
    # Row 1, col 3 -> safe
    assert is_safe(queens, 1, 3)


def test_n_queens_solutions_count():
    tracer = RecursionTracer(max_events=5000)

    # N=4 has 2 distinct solutions
    sols_4 = run_n_queens(4, tracer)
    assert len(sols_4) == 2

    # N=5 has 10 solutions
    sols_5 = run_n_queens(5, tracer)
    assert len(sols_5) == 10

    # N=8 has 92 solutions
    sols_8 = run_n_queens(8, tracer)
    assert len(sols_8) == 92


def test_n_queens_validity():
    tracer = RecursionTracer()
    solutions = run_n_queens(4, tracer)
    for sol in solutions:
        assert len(sol) == 4
        for r in range(4):
            assert is_safe(sol, r, sol[r])


def test_n_queens_invalid_n():
    tracer = RecursionTracer()
    with pytest.raises(ValueError):
        run_n_queens(3, tracer)
    with pytest.raises(ValueError):
        run_n_queens(9, tracer)
