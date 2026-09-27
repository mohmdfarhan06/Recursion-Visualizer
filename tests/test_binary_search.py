"""
Unit tests for Binary Search algorithm.
"""

import pytest
from core.tracer import RecursionTracer
from algorithms.binary_search import run_binary_search


def test_binary_search_found():
    tracer = RecursionTracer()
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    assert run_binary_search(arr, 23, tracer) == 5
    assert run_binary_search(arr, 2, tracer) == 0
    assert run_binary_search(arr, 91, tracer) == 9


def test_binary_search_not_found():
    tracer = RecursionTracer()
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    assert run_binary_search(arr, 100, tracer) == -1
    assert run_binary_search(arr, 1, tracer) == -1
    assert run_binary_search(arr, 15, tracer) == -1


def test_binary_search_unsorted_error():
    tracer = RecursionTracer()
    unsorted_arr = [5, 2, 8, 1]
    with pytest.raises(ValueError, match="sorted"):
        run_binary_search(unsorted_arr, 2, tracer)


def test_binary_search_invalid_inputs():
    tracer = RecursionTracer()
    with pytest.raises(ValueError):
        run_binary_search([], 5, tracer)
    with pytest.raises(ValueError):
        run_binary_search("not_a_list", 5, tracer)  # type: ignore
