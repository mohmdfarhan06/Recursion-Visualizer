"""
Matplotlib embedded visualizer for rendering recursion tree graphs.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from core.tree_model import TreeNode


class TreeVisualizerCanvas(ttk.Frame):
    """
    Tkinter widget embedding a Matplotlib canvas to render recursion trees.
    """

    # Theme palette (Catppuccin Mocha inspired)
    COLOR_BG = "#181825"
    COLOR_EDGE = "#6c7086"
    COLOR_PENDING_BG = "#313244"
    COLOR_PENDING_TEXT = "#cdd6f4"
    COLOR_ACTIVE_BG = "#fab387"
    COLOR_ACTIVE_BORDER = "#f9e2af"
    COLOR_ACTIVE_TEXT = "#11111b"
    COLOR_COMPLETED_BG = "#a6e3a1"
    COLOR_COMPLETED_TEXT = "#11111b"

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)

        self.figure = Figure(figsize=(6, 5), dpi=100, facecolor=self.COLOR_BG)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(self.COLOR_BG)
        self.ax.axis("off")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def draw_tree(self, visible_nodes: List[TreeNode], active_node: Optional[TreeNode]) -> None:
        """
        Renders the tree nodes and connecting edges.

        Args:
            visible_nodes: List of TreeNode instances visible at current step.
            active_node: The currently executing TreeNode (if any).
        """
        self.ax.clear()
        self.ax.set_facecolor(self.COLOR_BG)
        self.ax.axis("off")

        if not visible_nodes:
            self.ax.text(
                0.5, 0.5,
                "Ready. Click 'Start Visualization' to view recursion tree.",
                color="#a6adc8",
                ha="center", va="center",
                transform=self.ax.transAxes,
                fontsize=11,
                fontweight="bold"
            )
            self.canvas.draw_idle()
            return

        node_map = {n.call_id: n for n in visible_nodes}

        # Draw Edges
        for node in visible_nodes:
            if node.parent_id and node.parent_id in node_map:
                parent = node_map[node.parent_id]
                self.ax.plot(
                    [parent.x, node.x],
                    [parent.y, node.y],
                    color=self.COLOR_EDGE,
                    linestyle="-",
                    linewidth=1.8,
                    zorder=1
                )

        # Draw Nodes
        for node in visible_nodes:
            is_active = active_node and node.call_id == active_node.call_id

            if is_active:
                facecolor = self.COLOR_ACTIVE_BG
                edgecolor = self.COLOR_ACTIVE_BORDER
                textcolor = self.COLOR_ACTIVE_TEXT
                linewidth = 2.5
                fontweight = "bold"
            elif node.status == "completed":
                facecolor = self.COLOR_COMPLETED_BG
                edgecolor = "#a6e3a1"
                textcolor = self.COLOR_COMPLETED_TEXT
                linewidth = 1.2
                fontweight = "bold"
            else:
                facecolor = self.COLOR_PENDING_BG
                edgecolor = "#585b70"
                textcolor = self.COLOR_PENDING_TEXT
                linewidth = 1.0
                fontweight = "normal"

            # Draw circle marker node box
            bbox_props = dict(
                boxstyle="round,pad=0.4,rounding_size=0.3",
                facecolor=facecolor,
                edgecolor=edgecolor,
                linewidth=linewidth
            )

            label_text = node.label()
            self.ax.text(
                node.x, node.y,
                label_text,
                color=textcolor,
                ha="center", va="center",
                fontsize=9,
                fontweight=fontweight,
                bbox=bbox_props,
                zorder=2
            )

        # Adjust axes limits with padding
        xs = [n.x for n in visible_nodes]
        ys = [n.y for n in visible_nodes]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        padding_x = max(0.8, (x_max - x_min) * 0.15)
        padding_y = max(0.8, (y_max - y_min) * 0.15)

        self.ax.set_xlim(x_min - padding_x, x_max + padding_x)
        self.ax.set_ylim(y_min - padding_y, y_max + padding_y)

        self.canvas.draw_idle()

    def clear() -> None:
        """Clears the visualization canvas."""
        self.draw_tree([], None)
