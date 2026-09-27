"""
Core module for Recursion Visualizer: tracing engine, event definitions, data tree model, and playback.
"""

from core.events import EventType, TraceEvent
from core.tracer import RecursionTracer, MaxEventsExceededError
from core.tree_model import RecursionTreeModel, TreeNode
from core.playback import PlaybackController

__all__ = [
    "EventType",
    "TraceEvent",
    "RecursionTracer",
    "MaxEventsExceededError",
    "RecursionTreeModel",
    "TreeNode",
    "PlaybackController",
]
