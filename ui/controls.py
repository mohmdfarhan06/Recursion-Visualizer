"""
Control panel component containing algorithm selector, dynamic inputs, and playback buttons.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any


class ControlPanel(ttk.Frame):
    """
    Control panel widget for user interaction, input parameters, and playback controls.
    """

    ALGORITHMS = ["Fibonacci", "Factorial", "Binary Search", "N-Queens"]
    SPEEDS = ["Slow", "Normal", "Fast", "Ultra"]

    def __init__(
        self,
        parent: tk.Widget,
        on_algorithm_change: Callable[[str], None],
        on_start: Callable[[str, Dict[str, Any]], None],
        on_reset: Callable[[], None],
        on_prev: Callable[[], None],
        on_next: Callable[[], None],
        on_play: Callable[[], None],
        on_pause: Callable[[], None],
        on_speed_change: Callable[[str], None],
        **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.on_algorithm_change_cb = on_algorithm_change
        self.on_start_cb = on_start
        self.on_reset_cb = on_reset
        self.on_prev_cb = on_prev
        self.on_next_cb = on_next
        self.on_play_cb = on_play
        self.on_pause_cb = on_pause
        self.on_speed_change_cb = on_speed_change

        self.current_algo = tk.StringVar(value="Fibonacci")
        self.current_speed = tk.StringVar(value="Normal")

        # Input variables
        self.fib_n_var = tk.StringVar(value="5")
        self.fact_n_var = tk.StringVar(value="5")
        self.bs_arr_var = tk.StringVar(value="2, 5, 8, 12, 16, 23, 38, 56, 72, 91")
        self.bs_target_var = tk.StringVar(value="23")
        self.nq_n_var = tk.StringVar(value="4")

        self.input_frames: Dict[str, ttk.Frame] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        """Constructs widgets layout."""
        # Top Row: Algorithm selection & Dynamic inputs
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=8, pady=6)

        # Algorithm Selector
        lbl_algo = ttk.Label(top_frame, text="Algorithm:", font=("Segoe UI", 10, "bold"))
        lbl_algo.pack(side=tk.LEFT, padx=(0, 6))

        cbo_algo = ttk.Combobox(
            top_frame,
            textvariable=self.current_algo,
            values=self.ALGORITHMS,
            state="readonly",
            width=16,
            font=("Segoe UI", 9)
        )
        cbo_algo.pack(side=tk.LEFT, padx=(0, 16))
        cbo_algo.bind("<<ComboboxSelected>>", self._handle_algo_change)

        # Container for dynamic inputs
        self.dynamic_input_container = ttk.Frame(top_frame)
        self.dynamic_input_container.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self._create_input_frames()
        self._show_input_frame(self.current_algo.get())

        # Start & Reset buttons
        btn_start = ttk.Button(top_frame, text="⚡ Start Visualization", command=self._handle_start)
        btn_start.pack(side=tk.RIGHT, padx=4)

        btn_reset = ttk.Button(top_frame, text="🔄 Reset", command=self.on_reset_cb)
        btn_reset.pack(side=tk.RIGHT, padx=4)

        # Bottom Row: Playback Controls (Prev, Play, Pause, Next, Speed)
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill=tk.X, padx=8, pady=(2, 6))

        controls_sub = ttk.Frame(bottom_frame)
        controls_sub.pack(side=tk.LEFT)

        self.btn_prev = ttk.Button(controls_sub, text="⏮ Prev", width=8, command=self.on_prev_cb)
        self.btn_prev.pack(side=tk.LEFT, padx=3)

        self.btn_play = ttk.Button(controls_sub, text="▶ Play", width=8, command=self.on_play_cb)
        self.btn_play.pack(side=tk.LEFT, padx=3)

        self.btn_pause = ttk.Button(controls_sub, text="⏸ Pause", width=8, command=self.on_pause_cb)
        self.btn_pause.pack(side=tk.LEFT, padx=3)

        self.btn_next = ttk.Button(controls_sub, text="Next ⏭", width=8, command=self.on_next_cb)
        self.btn_next.pack(side=tk.LEFT, padx=3)

        # Speed selector
        speed_frame = ttk.Frame(bottom_frame)
        speed_frame.pack(side=tk.RIGHT)

        lbl_speed = ttk.Label(speed_frame, text="Speed:", font=("Segoe UI", 9, "bold"))
        lbl_speed.pack(side=tk.LEFT, padx=(0, 4))

        cbo_speed = ttk.Combobox(
            speed_frame,
            textvariable=self.current_speed,
            values=self.SPEEDS,
            state="readonly",
            width=8,
            font=("Segoe UI", 9)
        )
        cbo_speed.pack(side=tk.LEFT, padx=(0, 4))
        cbo_speed.bind("<<ComboboxSelected>>", lambda e: self.on_speed_change_cb(self.current_speed.get()))

    def _create_input_frames(self) -> None:
        """Creates dynamic input parameter fields for each algorithm."""
        # Fibonacci
        fib_f = ttk.Frame(self.dynamic_input_container)
        ttk.Label(fib_f, text="n (0-12):").pack(side=tk.LEFT, padx=(0, 4))
        ttk.Entry(fib_f, textvariable=self.fib_n_var, width=6).pack(side=tk.LEFT)
        self.input_frames["Fibonacci"] = fib_f

        # Factorial
        fact_f = ttk.Frame(self.dynamic_input_container)
        ttk.Label(fact_f, text="n (0-100):").pack(side=tk.LEFT, padx=(0, 4))
        ttk.Entry(fact_f, textvariable=self.fact_n_var, width=6).pack(side=tk.LEFT)
        self.input_frames["Factorial"] = fact_f

        # Binary Search
        bs_f = ttk.Frame(self.dynamic_input_container)
        ttk.Label(bs_f, text="Sorted Array:").pack(side=tk.LEFT, padx=(0, 4))
        ttk.Entry(bs_f, textvariable=self.bs_arr_var, width=32).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Label(bs_f, text="Target:").pack(side=tk.LEFT, padx=(0, 4))
        ttk.Entry(bs_f, textvariable=self.bs_target_var, width=6).pack(side=tk.LEFT)
        self.input_frames["Binary Search"] = bs_f

        # N-Queens
        nq_f = ttk.Frame(self.dynamic_input_container)
        ttk.Label(nq_f, text="Board Size N (4-8):").pack(side=tk.LEFT, padx=(0, 4))
        cbo_nq = ttk.Combobox(
            nq_f,
            textvariable=self.nq_n_var,
            values=["4", "5", "6", "7", "8"],
            state="readonly",
            width=4
        )
        cbo_nq.pack(side=tk.LEFT)
        self.input_frames["N-Queens"] = nq_f

    def _show_input_frame(self, algo_name: str) -> None:
        """Displays input fields corresponding to chosen algorithm."""
        for frame in self.input_frames.values():
            frame.pack_forget()
        if algo_name in self.input_frames:
            self.input_frames[algo_name].pack(side=tk.LEFT, fill=tk.X)

    def _handle_algo_change(self, event=None) -> None:
        algo = self.current_algo.get()
        self._show_input_frame(algo)
        self.on_algorithm_change_cb(algo)

    def _handle_start(self) -> None:
        algo = self.current_algo.get()
        params: Dict[str, Any] = {}

        if algo == "Fibonacci":
            params["n"] = self.fib_n_var.get()
        elif algo == "Factorial":
            params["n"] = self.fact_n_var.get()
        elif algo == "Binary Search":
            params["array_str"] = self.bs_arr_var.get()
            params["target_str"] = self.bs_target_var.get()
        elif algo == "N-Queens":
            params["n"] = self.nq_n_var.get()

        self.on_start_cb(algo, params)
