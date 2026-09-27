"""
Unit tests for core RecursionTracer, TreeModel, and PlaybackController logic.
"""

import pytest
from core.events import EventType
from core.tracer import RecursionTracer, MaxEventsExceededError
from core.tree_model import RecursionTreeModel
from core.playback import PlaybackController
from algorithms.fibonacci import run_fibonacci


def test_tracer_call_return_ordering():
    tracer = RecursionTracer()
    run_fibonacci(3, tracer)
    events = tracer.get_events()

    # Every CALL event must eventually have a corresponding RETURN event with matching call_id
    call_ids = [e.call_id for e in events if e.is_call]
    return_ids = [e.call_id for e in events if e.is_return]

    assert len(call_ids) == len(return_ids)
    assert set(call_ids) == set(return_ids)

    # Sequence numbers must be strictly increasing
    seq_nums = [e.seq_num for e in events]
    assert seq_nums == list(range(len(events)))


def test_parent_child_relationships():
    tracer = RecursionTracer()
    run_fibonacci(3, tracer)
    events = tracer.get_events()

    # Root event (call_id=1) must have parent_id=None
    root_call = next(e for e in events if e.call_id == 1 and e.is_call)
    assert root_call.parent_id is None

    # Child calls must reference a valid parent call_id
    call_events = [e for e in events if e.is_call]
    for call in call_events[1:]:
        assert call.parent_id is not None
        assert call.parent_id < call.call_id


def test_max_depth_tracking():
    tracer = RecursionTracer()
    run_fibonacci(4, tracer)
    # fib(4) depth: fib(4)->fib(3)->fib(2)->fib(1) => max_depth=4
    assert tracer.max_depth == 4


def test_max_events_exceeded():
    # Set a tiny max_events limit
    tracer = RecursionTracer(max_events=4)
    with pytest.raises(MaxEventsExceededError):
        run_fibonacci(5, tracer)


def test_playback_controller_stepping():
    tracer = RecursionTracer()
    run_fibonacci(3, tracer)
    events = tracer.get_events()

    playback = PlaybackController()
    playback.load_events(events)

    assert playback.total_steps == len(events)
    assert playback.current_step == 0

    # Step forward
    assert playback.step_forward() is True
    assert playback.current_step == 1

    # Jump to end
    playback.go_to_step(len(events) - 1)
    assert playback.current_step == len(events) - 1

    # Stepping forward past end returns False
    assert playback.step_forward() is False

    # Step backward
    assert playback.step_backward() is True
    assert playback.current_step == len(events) - 2

    # Reset
    playback.reset()
    assert playback.current_step == 0


def test_tree_model_state_reconstruction():
    tracer = RecursionTracer()
    run_fibonacci(3, tracer)
    events = tracer.get_events()

    tree_model = RecursionTreeModel(events)
    assert tree_model.root is not None
    assert tree_model.root.call_id == 1

    # Step 0: Root CALL fib(n=3)
    vis, stack, active, metrics = tree_model.get_state_at_step(0)
    assert len(vis) == 1
    assert len(stack) == 1
    assert active is not None and active.call_id == 1
    assert metrics["total_calls"] == 1
    assert metrics["completed_calls"] == 0

    # Last step: All calls completed
    vis, stack, active, metrics = tree_model.get_state_at_step(len(events) - 1)
    assert len(vis) == 5
    assert len(stack) == 0  # Stack empty when completed
    assert metrics["total_calls"] == 5
    assert metrics["completed_calls"] == 5
