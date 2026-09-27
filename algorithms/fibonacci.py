"""
Fibonacci algorithm with recursion tracing.
"""

from core.tracer import RecursionTracer


def fibonacci_recursive(n: int, tracer: RecursionTracer) -> int:
    """
    Recursively computes the nth Fibonacci number while recording tracing events.

    Args:
        n: Non-negative integer.
        tracer: RecursionTracer instance.

    Returns:
        int: nth Fibonacci number.
    """
    call_id = tracer.record_call(func_name="fib", args={"n": n})

    if n <= 0:
        res = 0
    elif n == 1:
        res = 1
    else:
        left = fibonacci_recursive(n - 1, tracer)
        right = fibonacci_recursive(n - 2, tracer)
        res = left + right

    tracer.record_return(call_id=call_id, return_value=res)
    return res


def run_fibonacci(n: int, tracer: RecursionTracer) -> int:
    """
    Validates input and runs traced recursive Fibonacci.

    Args:
        n: Target term (0 to 12).
        tracer: RecursionTracer instance.

    Returns:
        int: Computed result.

    Raises:
        ValueError: If n is invalid.
    """
    if not isinstance(n, int):
        raise ValueError("Input n must be an integer.")
    if n < 0 or n > 12:
        raise ValueError("Fibonacci input n must be between 0 and 12 for clean visualization.")

    tracer.reset()
    return fibonacci_recursive(n, tracer)
