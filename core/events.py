"""
Trace event definitions for the Recursion Visualizer engine.
"""

from enum import Enum
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field


class EventType(Enum):
    """Types of recursive tracing events."""
    CALL = "CALL"
    RETURN = "RETURN"


@dataclass
class TraceEvent:
    """
    Represents a single execution event in a recursive algorithm.

    Attributes:
        event_type: CALL or RETURN event.
        call_id: Unique integer identifier for the function call instance.
        parent_id: Identifier of the caller function, or None if root call.
        func_name: Name of the recursive function.
        args: Dictionary of function argument names and values.
        depth: Recursion depth (1-indexed for root).
        return_value: Value returned by function (populated on RETURN event).
        seq_num: Sequential event index across execution.
        extra_info: Optional algorithm-specific metadata (e.g., board state, interval bounds).
    """
    event_type: EventType
    call_id: int
    parent_id: Optional[int]
    func_name: str
    args: Dict[str, Any]
    depth: int
    return_value: Any = None
    seq_num: int = 0
    extra_info: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_call(self) -> bool:
        return self.event_type == EventType.CALL

    @property
    def is_return(self) -> bool:
        return self.event_type == EventType.RETURN

    def format_args(self) -> str:
        """Returns a concise string representation of function arguments."""
        items = []
        for k, v in self.args.items():
            if isinstance(v, list) and len(v) > 6:
                v_str = f"[{', '.join(map(str, v[:3]))}, ..., {', '.join(map(str, v[-2:]))}]"
            else:
                v_str = repr(v)
            items.append(f"{k}={v_str}")
        return ", ".join(items)

    def format_call(self) -> str:
        """Formats the call signature like `fib(n=5)`."""
        return f"{self.func_name}({self.format_args()})"
