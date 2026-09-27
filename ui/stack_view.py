"""
Call stack visualization panel component.
"""

import tkinter as tk
from tkinter import ttk
from typing import List
from core.tree_model import TreeNode


class CallStackView(ttk.Frame):
    """
    Panel widget displaying active function call stack frames in top-down order.
    """

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)

        self._build_ui()

    def _build_ui(self) -> None:
        """Constructs stack view header and list container."""
        # Header
        hdr_frame = ttk.Frame(self)
        hdr_frame.pack(fill=tk.X, padx=6, pady=(6, 2))

        lbl_title = ttk.Label(hdr_frame, text="🥞 Call Stack (Top -> Bottom)", font=("Segoe UI", 10, "bold"))
        lbl_title.pack(side=tk.LEFT)

        # Container frame with canvas & scrollbar for clean custom cards
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        self.tree = ttk.Treeview(
            container,
            columns=("depth", "call_id", "signature"),
            show="headings",
            selectmode="none"
        )
        self.tree.heading("depth", text="Depth")
        self.tree.heading("call_id", text="Call ID")
        self.tree.heading("signature", text="Function Call")

        self.tree.column("depth", width=55, anchor="center")
        self.tree.column("call_id", width=65, anchor="center")
        self.tree.column("signature", width=220, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure visual tags for top of stack frame highlighting
        self.tree.tag_configure("top_frame", background="#45475a", foreground="#fab387", font=("Consolas", 9, "bold"))
        self.tree.tag_configure("stack_frame", background="#252538", foreground="#cdd6f4", font=("Consolas", 9))

    def update_stack(self, active_stack_nodes: List[TreeNode]) -> None:
        """
        Updates the displayed stack frames.

        Args:
            active_stack_nodes: List of open TreeNode instances (root to top).
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not active_stack_nodes:
            return

        # Reverse list so top of stack is displayed first
        reversed_stack = list(reversed(active_stack_nodes))

        for idx, node in enumerate(reversed_stack):
            is_top = (idx == 0)
            tag = "top_frame" if is_top else "stack_frame"

            depth_str = f"Depth {node.depth}"
            call_id_str = f"#{node.call_id}"
            sig_str = f"{node.func_name}({node.format_args()})"
            if is_top:
                sig_str = f"➡️ {sig_str}  (ACTIVE)"

            self.tree.insert(
                "",
                tk.END,
                values=(depth_str, call_id_str, sig_str),
                tags=(tag,)
            )
