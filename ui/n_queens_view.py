"""
Dedicated Tkinter Canvas chessboard visualization for N-Queens algorithm.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, List
from core.events import TraceEvent


class NQueensCanvas(ttk.Frame):
    """
    Renders the N-Queens chessboard state, queen placements, row/col highlights,
    and solution counters on a Tkinter Canvas.
    """

    COLOR_BG = "#181825"
    COLOR_LIGHT_SQ = "#b4bebe"
    COLOR_DARK_SQ = "#45475a"
    COLOR_ACTIVE_SQ = "#fab387"
    COLOR_QUEEN = "#f38ba8"
    COLOR_QUEEN_TEXT = "#11111b"
    COLOR_HIGHLIGHT_BORDER = "#f9e2af"

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)

        self._build_ui()

    def _build_ui(self) -> None:
        """Sets up the canvas and info header."""
        self.hdr_label = ttk.Label(
            self,
            text="♛ N-Queens Chessboard State",
            font=("Segoe UI", 11, "bold")
        )
        self.hdr_label.pack(anchor="w", padx=8, pady=(6, 2))

        self.canvas = tk.Canvas(
            self,
            bg=self.COLOR_BG,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.canvas.bind("<Configure>", lambda e: self.redraw())

        self.current_event: Optional[TraceEvent] = None
        self.current_extra: Dict[str, Any] = {}

    def update_state(self, event: Optional[TraceEvent]) -> None:
        """
        Updates canvas drawing based on current trace event.

        Args:
            event: The TraceEvent at current playback step.
        """
        self.current_event = event
        self.current_extra = event.extra_info if event else {}
        self.redraw()

    def redraw(self) -> None:
        """Redraws the chessboard grid and queens."""
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 50 or height < 50:
            return

        extra = self.current_extra
        n = extra.get("board_size", 4)
        queens: List[int] = extra.get("queens", [-1] * n)
        curr_row = extra.get("row", -1)
        curr_col = extra.get("col", -1)
        solutions_count = extra.get("solutions_found", 0)

        # Calculate square size and offsets to center board
        margin = 40
        board_size_px = min(width - margin * 2, height - margin * 2 - 30)
        board_size_px = max(board_size_px, 100)
        sq_size = board_size_px / n

        offset_x = (width - board_size_px) / 2
        offset_y = (height - board_size_px - 30) / 2 + 20

        # Draw Title & Solution Count info
        info_text = f"Board Size: {n}x{n}  |  Solutions Found: {solutions_count}"
        if self.current_event:
            if self.current_event.is_call:
                info_text += f"  |  Exploring Row {curr_row}"
            else:
                info_text += f"  |  Backtracking / Returning from Row {curr_row}"

        self.canvas.create_text(
            width / 2, offset_y - 14,
            text=info_text,
            fill="#cdd6f4",
            font=("Segoe UI", 10, "bold")
        )

        # Draw Grid Squares
        for r in range(n):
            for c in range(n):
                x1 = offset_x + c * sq_size
                y1 = offset_y + r * sq_size
                x2 = x1 + sq_size
                y2 = y1 + sq_size

                is_dark = (r + c) % 2 == 1
                bg_color = self.COLOR_DARK_SQ if is_dark else self.COLOR_LIGHT_SQ

                # Highlight currently evaluated cell
                is_active = (r == curr_row and c == curr_col)
                if is_active:
                    bg_color = self.COLOR_ACTIVE_SQ

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=bg_color,
                    outline="#313244",
                    width=1
                )

                if is_active:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline=self.COLOR_HIGHLIGHT_BORDER,
                        width=3
                    )

                # Draw Queen if placed in this row and column
                if r < len(queens) and queens[r] == c:
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    radius = sq_size * 0.35

                    # Draw Queen circle background
                    self.canvas.create_oval(
                        center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        fill=self.COLOR_QUEEN,
                        outline="#ffffff",
                        width=2
                    )

                    # Draw Queen '♛' crown text
                    font_size = int(sq_size * 0.45)
                    self.canvas.create_text(
                        center_x, center_y,
                        text="♛",
                        fill=self.COLOR_QUEEN_TEXT,
                        font=("Segoe UI Symbol", max(10, font_size), "bold")
                    )

        # Draw Row & Column labels
        for i in range(n):
            # Row index on left
            rx = offset_x - 14
            ry = offset_y + (i + 0.5) * sq_size
            self.canvas.create_text(rx, ry, text=str(i), fill="#a6adc8", font=("Consolas", 10, "bold"))

            # Column index on top
            cx = offset_x + (i + 0.5) * sq_size
            cy = offset_y - 12
            self.canvas.create_text(cx, cy, text=str(i), fill="#a6adc8", font=("Consolas", 10, "bold"))
