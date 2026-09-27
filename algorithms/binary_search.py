"""
Binary search algorithm with recursion tracing.
"""

from typing import List
from core.tracer import RecursionTracer


def binary_search_recursive(arr: List[int], low: int, high: int, target: int, tracer: RecursionTracer) -> int:
    """
    Recursively searches for target in sorted array arr[low..high].

    Args:
        arr: Sorted integer list.
        low: Search range lower index bound.
        high: Search range upper index bound.
        target: Target integer to locate.
        tracer: RecursionTracer instance.

    Returns:
        int: Index of target if found, else -1.
    """
    extra = {
        "low": low,
        "high": high,
        "mid": (low + high) // 2 if low <= high else -1,
        "target": target
    }
    call_id = tracer.record_call(
        func_name="binary_search",
        args={"low": low, "high": high, "target": target},
        extra_info=extra
    )

    if low > high:
        res = -1
    else:
        mid = (low + high) // 2
        extra["mid"] = mid

        if arr[mid] == target:
            res = mid
        elif arr[mid] > target:
            res = binary_search_recursive(arr, low, mid - 1, target, tracer)
        else:
            res = binary_search_recursive(arr, mid + 1, high, target, tracer)

    tracer.record_return(call_id=call_id, return_value=res, extra_info=extra)
    return res


def run_binary_search(arr: List[int], target: int, tracer: RecursionTracer) -> int:
    """
    Validates array sortedness and performs traced recursive binary search.

    Args:
        arr: List of integers.
        target: Target integer.
        tracer: RecursionTracer instance.

    Returns:
        int: Found index or -1.

    Raises:
        ValueError: If input format is invalid or array is unsorted.
    """
    if not isinstance(arr, list):
        raise ValueError("Input array must be a list of integers.")
    if not arr:
        raise ValueError("Array cannot be empty.")
    if not all(isinstance(x, int) for x in arr):
        raise ValueError("All array elements must be integers.")
    if not isinstance(target, int):
        raise ValueError("Target must be an integer.")

    # Check sortedness
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            raise ValueError("Input array must be sorted in non-decreasing order.")

    tracer.reset()
    return binary_search_recursive(arr, 0, len(arr) - 1, target, tracer)
