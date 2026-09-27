"""
Deterministic recursion tracing engine.
"""

from typing import Any, Dict, List, Optional
from core.events import EventType, TraceEvent


class MaxEventsExceededError(Exception):
    """Exception raised when recursive execution exceeds configured maximum event count."""
    pass


class RecursionTracer:
    """
    Records deterministic execution events (CALL and RETURN) for recursive functions.

    Maintains internal call stack state to dynamically associate child calls
    with parent call IDs and compute recursion depth.
    """

    def __init__(self, max_events: int = 5000):
        """
        Initialize tracer with a safety cap on maximum event trace length.

        Args:
            max_events: Maximum allowed events before throwing MaxEventsExceededError.
        """
        self.max_events = max_events
        self.events: List[TraceEvent] = []
        self._call_stack: List[int] = []  # Stack of call_ids
        self._call_counter = 0
        self._seq_counter = 0
        self._max_depth = 0

    def reset(self) -> None:
        """Resets all internal tracer state."""
        self.events.clear()
        self._call_stack.clear()
        self._call_counter = 0
        self._seq_counter = 0
        self._max_depth = 0

    def record_call(self, func_name: str, args: Dict[str, Any], extra_info: Optional[Dict[str, Any]] = None) -> int:
        """
        Records a recursive function entry (CALL event).

        Args:
            func_name: Name of the function being invoked.
            args: Dictionary of input parameters.
            extra_info: Optional extra metadata (e.g., board state).

        Returns:
            int: The assigned call_id for this function invocation.

        Raises:
            MaxEventsExceededError: If maximum events limit is reached.
        """
        if len(self.events) >= self.max_events:
            raise MaxEventsExceededError(
                f"Recursion exceeded maximum limit of {self.max_events} events. "
                f"Try reducing the input size."
            )

        self._call_counter += 1
        call_id = self._call_counter
        parent_id = self._call_stack[-1] if self._call_stack else None
        depth = len(self._call_stack) + 1

        if depth > self._max_depth:
            self._max_depth = depth

        event = TraceEvent(
            event_type=EventType.CALL,
            call_id=call_id,
            parent_id=parent_id,
            func_name=func_name,
            args=args,
            depth=depth,
            return_value=None,
            seq_num=self._seq_counter,
            extra_info=extra_info or {}
        )

        self._seq_counter += 1
        self.events.append(event)
        self._call_stack.append(call_id)
        return call_id

    def record_return(self, call_id: int, return_value: Any, extra_info: Optional[Dict[str, Any]] = None) -> TraceEvent:
        """
        Records a recursive function exit (RETURN event).

        Args:
            call_id: The identifier returned by record_call.
            return_value: Output value returned by the function.
            extra_info: Optional metadata at return time.

        Returns:
            TraceEvent: The created RETURN trace event.

        Raises:
            MaxEventsExceededError: If maximum events limit is reached.
            ValueError: If call stack state is inconsistent.
        """
        if len(self.events) >= self.max_events:
            raise MaxEventsExceededError(
                f"Recursion exceeded maximum limit of {self.max_events} events."
            )

        if not self._call_stack or self._call_stack[-1] != call_id:
            raise ValueError(
                f"Invalid tracer return state: expected call_id {self._call_stack[-1] if self._call_stack else None}, "
                f"got {call_id}"
            )

        # Find matching call event to get function name, args, depth, parent_id
        call_event = next((e for e in reversed(self.events) if e.call_id == call_id and e.is_call), None)
        if not call_event:
            raise ValueError(f"No matching CALL event found for call_id {call_id}")

        event = TraceEvent(
            event_type=EventType.RETURN,
            call_id=call_id,
            parent_id=call_event.parent_id,
            func_name=call_event.func_name,
            args=call_event.args,
            depth=call_event.depth,
            return_value=return_value,
            seq_num=self._seq_counter,
            extra_info=extra_info or call_event.extra_info
        )

        self._seq_counter += 1
        self.events.append(event)
        self._call_stack.pop()
        return event

    def trace(self, func_name: str, **args):
        """
        Helper context manager or decorator for tracing explicit scopes if desired.
        """
        class TraceContext:
            def __init__(ctx_self, tracer_obj: 'RecursionTracer'):
                ctx_self.tracer = tracer_obj
                ctx_self.call_id = None

            def __enter__(ctx_self):
                ctx_self.call_id = ctx_self.tracer.record_call(func_name, args)
                return ctx_self.call_id

            def __exit__(ctx_self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    # Normal return - caller should ideally call record_return, but context can backup return None
                    pass
                return False
        return TraceContext(self)

    @property
    def total_calls(self) -> int:
        """Returns total distinct function calls recorded."""
        return self._call_counter

    @property
    def max_depth(self) -> int:
        """Returns the maximum recursion depth reached."""
        return self._max_depth

    def get_events(self) -> List[TraceEvent]:
        """Returns a copy of all recorded events."""
        return list(self.events)
