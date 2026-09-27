"""
Playback controller for stepping through execution events.
"""

from typing import Callable, List, Optional
from core.events import TraceEvent


class PlaybackController:
    """
    Manages playback state, stepping, auto-play intervals, and subscriber notifications.
    """

    SPEED_DELAYS = {
        "Slow": 1000,     # 1.0s delay
        "Normal": 400,    # 0.4s delay
        "Fast": 100,      # 0.1s delay
        "Ultra": 20       # 0.02s delay
    }

    def __init__(self, events: Optional[List[TraceEvent]] = None):
        self.events: List[TraceEvent] = events or []
        self.current_step: int = -1  # -1 before start, 0..len(events)-1
        self.is_playing: bool = False
        self.speed_name: str = "Normal"
        self._listeners: List[Callable[[int, int, Optional[TraceEvent]], None]] = []

    def load_events(self, events: List[TraceEvent]) -> None:
        """Loads a new event trace into the controller."""
        self.pause()
        self.events = list(events)
        self.current_step = 0 if self.events else -1
        self.notify_listeners()

    def add_listener(self, listener: Callable[[int, int, Optional[TraceEvent]], None]) -> None:
        """Registers a listener callback: fn(current_step, total_steps, current_event)."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[int, int, Optional[TraceEvent]], None]) -> None:
        """Unregisters a listener callback."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def notify_listeners(self) -> None:
        """Notifies all registered listeners of the current step state."""
        total = len(self.events)
        curr_ev = self.current_event
        for listener in self._listeners:
            listener(self.current_step, total, curr_ev)

    @property
    def total_steps(self) -> int:
        return len(self.events)

    @property
    def current_event(self) -> Optional[TraceEvent]:
        if 0 <= self.current_step < len(self.events):
            return self.events[self.current_step]
        return None

    @property
    def speed_delay_ms(self) -> int:
        return self.SPEED_DELAYS.get(self.speed_name, 400)

    def set_speed(self, speed_name: str) -> None:
        """Sets playback speed preset."""
        if speed_name in self.SPEED_DELAYS:
            self.speed_name = speed_name

    def step_forward(self) -> bool:
        """
        Advances playback by one event step.

        Returns:
            bool: True if advanced, False if already at end.
        """
        if not self.events:
            return False

        if self.current_step < len(self.events) - 1:
            self.current_step += 1
            self.notify_listeners()
            return True
        else:
            self.pause()
            return False

    def step_backward(self) -> bool:
        """
        Rewinds playback by one event step.

        Returns:
            bool: True if rewound, False if already at start.
        """
        if not self.events:
            return False

        if self.current_step > 0:
            self.current_step -= 1
            self.notify_listeners()
            return True
        return False

    def play(self) -> None:
        """Starts auto-play."""
        if self.events and self.current_step < len(self.events) - 1:
            self.is_playing = True

    def pause(self) -> None:
        """Pauses auto-play."""
        self.is_playing = False

    def reset(self) -> None:
        """Resets playback to initial step (step 0)."""
        self.pause()
        if self.events:
            self.current_step = 0
        else:
            self.current_step = -1
        self.notify_listeners()

    def go_to_step(self, step_idx: int) -> None:
        """Jumps directly to a specific step index."""
        if not self.events:
            return
        target = min(max(0, step_idx), len(self.events) - 1)
        if target != self.current_step:
            self.current_step = target
            self.notify_listeners()
