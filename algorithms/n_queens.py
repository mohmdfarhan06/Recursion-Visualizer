"""
N-Queens recursive solver with execution tracing.
"""

from typing import List
from core.tracer import RecursionTracer


def is_safe(queens: List[int], row: int, col: int) -> bool:
    """
    Checks if placing a queen at (row, col) is valid given existing row placements.

    Args:
        queens: List where queens[r] is column of queen on row r.
        row: Target row index.
        col: Target column index.

    Returns:
        bool: True if safe, False if under attack.
    """
    for r in range(row):
        c = queens[r]
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True


def solve_n_queens_recursive(
    n: int,
    row: int,
    queens: List[int],
    solutions: List[List[int]],
    tracer: RecursionTracer
) -> int:
    """
    Recursively solves N-Queens problem for row `row` while recording events.

    Args:
        n: Board size.
        row: Current row index to place a queen.
        queens: List of size n storing column placements for rows 0..row-1.
        solutions: Collector list for completed valid board placement lists.
        tracer: RecursionTracer instance.

    Returns:
        int: Number of solutions found in this subtree.
    """
    extra = {
        "board_size": n,
        "row": row,
        "queens": list(queens),
        "solutions_found": len(solutions)
    }

    call_id = tracer.record_call(
        func_name="solve_row",
        args={"row": row, "placed": list(queens[:row])},
        extra_info=extra
    )

    subtree_solutions = 0

    if row == n:
        # Base case: All queens successfully placed!
        solutions.append(list(queens))
        subtree_solutions = 1
        extra["solutions_found"] = len(solutions)
        extra["queens"] = list(queens)
    else:
        for col in range(n):
            if is_safe(queens, row, col):
                queens[row] = col
                extra["col"] = col
                extra["queens"] = list(queens)

                found = solve_n_queens_recursive(n, row + 1, queens, solutions, tracer)
                subtree_solutions += found

                # Reset placement for backtrack step
                queens[row] = -1

    extra["solutions_found"] = len(solutions)
    tracer.record_return(call_id=call_id, return_value=subtree_solutions, extra_info=extra)
    return subtree_solutions


def run_n_queens(n: int, tracer: RecursionTracer) -> List[List[int]]:
    """
    Validates board size and executes traced N-Queens solver.

    Args:
        n: Board size N (4 to 8).
        tracer: RecursionTracer instance.

    Returns:
        List[List[int]]: List of solution board placements.

    Raises:
        ValueError: If n is not between 4 and 8.
    """
    if not isinstance(n, int):
        raise ValueError("Board size N must be an integer.")
    if n < 4 or n > 8:
        raise ValueError("N-Queens board size must be between 4 and 8.")

    tracer.reset()
    solutions: List[List[int]] = []
    queens = [-1] * n

    solve_n_queens_recursive(n, 0, queens, solutions, tracer)
    return solutions
