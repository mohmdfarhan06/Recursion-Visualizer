"""
Factorial algorithm with recursion tracing.
"""

from core.tracer import RecursionTracer


def factorial_recursive(n: int, tracer: RecursionTracer) -> int:
    """
    Recursively computes n! while recording tracing events.

    Args:
        n: Non-negative integer.
        tracer: RecursionTracer instance.

    Returns:
        int: n!
    """
    call_id = tracer.record_call(func_name="factorial", args={"n": n})

    if n <= 1:
        res = 1
    else:
        sub_res = factorial_recursive(n - 1, tracer)
        res = n * sub_res

    tracer.record_return(call_id=call_id, return_value=res)
    return res


def run_factorial(n: int, tracer: RecursionTracer) -> int:
    """
    Validates input and executes traced recursive Factorial.

    Args:
        n: Integer between 0 and 100.
        tracer: RecursionTracer instance.

    Returns:
        int: n!

    Raises:
        ValueError: If n is out of valid bounds.
    """
    if not isinstance(n, int):
        raise ValueError("Input n must be an integer.")
    if n < 0 or n > 100:
        raise ValueError("Factorial input n must be between 0 and 100.")

    tracer.reset()
    return factorial_recursive(n, tracer)
