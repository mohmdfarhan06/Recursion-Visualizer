"""
Main application window and integration layout for Recursion Visualizer.
"""

import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional

from core.tracer import RecursionTracer, MaxEventsExceededError
from core.tree_model import RecursionTreeModel
from core.playback import PlaybackController
from core.events import TraceEvent

from algorithms.fibonacci import run_fibonacci
from algorithms.factorial import run_factorial
from algorithms.binary_search import run_binary_search
from algorithms.n_queens import run_n_queens

from ui.controls import ControlPanel
from ui.tree_view import TreeVisualizerCanvas
from ui.stack_view import CallStackView
from ui.n_queens_view import NQueensCanvas


class RecursionVisualizerApp(tk.Tk):
    """
    Main Tkinter Desktop Application for Recursion Visualizer.
    """

    def __init__(self):
        super().__init__()

        self.title("Recursion Visualizer")
        self.geometry("1120x760")
        self.minsize(960, 640)

        # Apply dark theme styling
        self._setup_theme()

        # Engine instances
        self.tracer = RecursionTracer(max_events=5000)
        self.playback = PlaybackController()
        self.tree_model: Optional[RecursionTreeModel] = None

        # State tracking
        self.current_algo = "Fibonacci"
        self._auto_play_job: Optional[str] = None
        self._start_time: float = 0.0

        # UI Components
        self._build_header()
        self._build_controls()
        self._build_main_view()
        self._build_status_bar()

        # Register playback subscriber
        self.playback.add_listener(self._on_playback_step)

    def _setup_theme(self) -> None:
        """Applies custom dark theme colors using ttk styles."""
        self.configure(bg="#181825")

        style = ttk.Style(self)
        style.theme_use("clam")

        # Palette definition
        bg_dark = "#181825"
        panel_bg = "#1e1e2e"
        accent_blue = "#89b4fa"
        fg_text = "#cdd6f4"

        style.configure(".", background=bg_dark, foreground=fg_text, font=("Segoe UI", 9))

        # Frames & PanedWindow
        style.configure("TFrame", background=bg_dark)
        style.configure("Panel.TFrame", background=panel_bg)
        style.configure("TPanedwindow", background=bg_dark)

        # Labels
        style.configure("TLabel", background=bg_dark, foreground=fg_text)
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=accent_blue)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#a6adc8")
        style.configure("Status.TLabel", font=("Consolas", 9, "bold"), foreground="#fab387")

        # Buttons
        style.configure(
            "TButton",
            background="#313244",
            foreground=fg_text,
            bordercolor="#45475a",
            focusthickness=3,
            focuscolor=accent_blue,
            padding=5
        )
        style.map(
            "TButton",
            background=[("active", "#45475a"), ("disabled", "#1e1e2e")],
            foreground=[("disabled", "#585b70")]
        )

        # Combobox & Entry
        style.configure("TCombobox", fieldbackground="#313244", background="#313244", foreground=fg_text)
        style.configure("TEntry", fieldbackground="#313244", foreground=fg_text, insertcolor=fg_text)

        # Treeview (Call Stack)
        style.configure(
            "Treeview",
            background="#252538",
            fieldbackground="#252538",
            foreground=fg_text,
            rowheight=24,
            font=("Consolas", 9)
        )
        style.configure(
            "Treeview.Heading",
            background="#313244",
            foreground=accent_blue,
            font=("Segoe UI", 9, "bold")
        )

    def _build_header(self) -> None:
        """Renders header banner."""
        hdr_frame = ttk.Frame(self, style="Panel.TFrame")
        hdr_frame.pack(fill=tk.X, padx=10, pady=(10, 4))

        title_lbl = ttk.Label(
            hdr_frame,
            text="🌳 Recursion Visualizer",
            style="Header.TLabel",
            background="#1e1e2e"
        )
        title_lbl.pack(anchor="w", padx=12, pady=(8, 2))

        sub_lbl = ttk.Label(
            hdr_frame,
            text="Interactive step-by-step execution tracer and call stack visualizer for DSA algorithms.",
            style="SubHeader.TLabel",
            background="#1e1e2e"
        )
        sub_lbl.pack(anchor="w", padx=12, pady=(0, 8))

    def _build_controls(self) -> None:
        """Instantiates controls panel."""
        ctrl_frame = ttk.Frame(self, style="Panel.TFrame")
        ctrl_frame.pack(fill=tk.X, padx=10, pady=4)

        self.control_panel = ControlPanel(
            ctrl_frame,
            on_algorithm_change=self._on_algo_changed,
            on_start=self._on_start_clicked,
            on_reset=self._on_reset_clicked,
            on_prev=self._on_prev_clicked,
            on_next=self._on_next_clicked,
            on_play=self._on_play_clicked,
            on_pause=self._on_pause_clicked,
            on_speed_change=self._on_speed_changed
        )
        self.control_panel.pack(fill=tk.X, padx=4, pady=4)

    def _build_main_view(self) -> None:
        """Constructs split-panel container for tree graph and call stack."""
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        # Left Container: Holds Matplotlib Tree Canvas OR N-Queens Canvas
        self.left_container = ttk.Frame(self.paned, style="Panel.TFrame")

        self.tree_view = TreeVisualizerCanvas(self.left_container)
        self.tree_view.pack(fill=tk.BOTH, expand=True)

        self.nq_view = NQueensCanvas(self.left_container)
        # Initially hidden, shown when N-Queens is selected

        self.paned.add(self.left_container, weight=3)

        # Right Container: Call Stack
        self.right_container = ttk.Frame(self.paned, style="Panel.TFrame")
        self.stack_view = CallStackView(self.right_container)
        self.stack_view.pack(fill=tk.BOTH, expand=True)

        self.paned.add(self.right_container, weight=1)

    def _build_status_bar(self) -> None:
        """Constructs bottom status & metrics bar."""
        status_frame = ttk.Frame(self, style="Panel.TFrame")
        status_frame.pack(fill=tk.X, padx=10, pady=(4, 10))

        self.lbl_calls = ttk.Label(status_frame, text="Total Calls: 0", style="Status.TLabel", background="#1e1e2e")
        self.lbl_calls.pack(side=tk.LEFT, padx=14, pady=6)

        self.lbl_curr_depth = ttk.Label(status_frame, text="Current Depth: 0", style="Status.TLabel", background="#1e1e2e")
        self.lbl_curr_depth.pack(side=tk.LEFT, padx=14, pady=6)

        self.lbl_max_depth = ttk.Label(status_frame, text="Max Depth: 0", style="Status.TLabel", background="#1e1e2e")
        self.lbl_max_depth.pack(side=tk.LEFT, padx=14, pady=6)

        self.lbl_completed = ttk.Label(status_frame, text="Completed Calls: 0", style="Status.TLabel", background="#1e1e2e")
        self.lbl_completed.pack(side=tk.LEFT, padx=14, pady=6)

        self.lbl_step_info = ttk.Label(status_frame, text="Step: 0 / 0", style="Status.TLabel", background="#1e1e2e")
        self.lbl_step_info.pack(side=tk.RIGHT, padx=14, pady=6)

    def _on_algo_changed(self, algo_name: str) -> None:
        """Handles switching algorithms."""
        self._stop_auto_play()
        self.current_algo = algo_name

        # Switch left panel view based on algorithm selection
        if algo_name == "N-Queens":
            self.tree_view.pack_forget()
            self.nq_view.pack(fill=tk.BOTH, expand=True)
        else:
            self.nq_view.pack_forget()
            self.tree_view.pack(fill=tk.BOTH, expand=True)

        self._on_reset_clicked()

    def _on_start_clicked(self, algo_name: str, params: Dict[str, Any]) -> None:
        """Runs the chosen algorithm, records trace events, and loads playback."""
        self._stop_auto_play()
        self.current_algo = algo_name

        try:
            self._start_time = time.time()

            if algo_name == "Fibonacci":
                n = int(params["n"])
                run_fibonacci(n, self.tracer)
            elif algo_name == "Factorial":
                n = int(params["n"])
                run_factorial(n, self.tracer)
            elif algo_name == "Binary Search":
                raw_arr = params["array_str"]
                arr = [int(x.strip()) for x in raw_arr.split(",") if x.strip()]
                target = int(params["target_str"])
                run_binary_search(arr, target, self.tracer)
            elif algo_name == "N-Queens":
                n = int(params["n"])
                run_n_queens(n, self.tracer)

            events = self.tracer.get_events()
            if not events:
                messagebox.showwarning("Warning", "No execution events generated.")
                return

            self.tree_model = RecursionTreeModel(events)
            self.playback.load_events(events)

        except MaxEventsExceededError as e:
            messagebox.showerror("Execution Limit Exceeded", str(e))
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred during execution:\n{e}")

    def _on_playback_step(self, step_idx: int, total_steps: int, current_event: Optional[TraceEvent]) -> None:
        """Callback invoked whenever playback position changes."""
        self.lbl_step_info.config(text=f"Step: {max(0, step_idx + 1)} / {total_steps}")

        if not self.tree_model or step_idx < 0:
            self.tree_view.draw_tree([], None)
            self.stack_view.update_stack([])
            self.nq_view.update_state(None)
            self._update_metrics({"total_calls": 0, "completed_calls": 0, "current_depth": 0, "max_depth": 0})
            return

        visible_nodes, active_stack, active_node, metrics = self.tree_model.get_state_at_step(step_idx)

        # Update Views
        if self.current_algo == "N-Queens":
            self.nq_view.update_state(current_event)
        else:
            self.tree_view.draw_tree(visible_nodes, active_node)

        self.stack_view.update_stack(active_stack)
        self._update_metrics(metrics)

    def _update_metrics(self, metrics: Dict[str, Any]) -> None:
        """Updates metrics label values."""
        self.lbl_calls.config(text=f"Total Calls: {metrics['total_calls']}")
        self.lbl_curr_depth.config(text=f"Current Depth: {metrics['current_depth']}")
        self.lbl_max_depth.config(text=f"Max Depth: {metrics['max_depth']}")
        self.lbl_completed.config(text=f"Completed Calls: {metrics['completed_calls']}")

    def _on_prev_clicked(self) -> None:
        self._stop_auto_play()
        self.playback.step_backward()

    def _on_next_clicked(self) -> None:
        self._stop_auto_play()
        self.playback.step_forward()

    def _on_play_clicked(self) -> None:
        if not self.playback.events:
            return
        if self.playback.current_step >= len(self.playback.events) - 1:
            self.playback.reset()

        self.playback.play()
        self._schedule_auto_play_tick()

    def _on_pause_clicked(self) -> None:
        self._stop_auto_play()

    def _on_reset_clicked(self) -> None:
        self._stop_auto_play()
        self.playback.reset()

    def _on_speed_changed(self, speed_name: str) -> None:
        self.playback.set_speed(speed_name)

    def _stop_auto_play(self) -> None:
        """Cancels scheduled after() playback loop."""
        self.playback.pause()
        if self._auto_play_job is not None:
            self.after_cancel(self._auto_play_job)
            self._auto_play_job = None

    def _schedule_auto_play_tick(self) -> None:
        """Schedules next step execution via Tkinter after()."""
        if self.playback.is_playing:
            delay = self.playback.speed_delay_ms
            self._auto_play_job = self.after(delay, self._auto_play_tick)

    def _auto_play_tick(self) -> None:
        """Executes single step in auto-play mode."""
        self._auto_play_job = None
        if self.playback.is_playing:
            advanced = self.playback.step_forward()
            if advanced:
                self._schedule_auto_play_tick()
            else:
                self.playback.pause()
