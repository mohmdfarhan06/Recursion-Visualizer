"""
Tree model for representing and layout-computing the recursion tree state.
"""

from typing import Dict, List, Optional, Tuple, Any
from core.events import EventType, TraceEvent


class TreeNode:
    """
    Represents a node in the recursion call tree.

    Attributes:
        call_id: Unique identifier for this call.
        parent_id: Call ID of parent node.
        func_name: Name of function.
        args: Function parameters.
        depth: Recursion depth (1-indexed).
        return_value: Output value once completed.
        children: List of child TreeNode instances.
        status: Visual state ('pending', 'active', 'completed').
        x: X-coordinate for plotting layout.
        y: Y-coordinate for plotting layout.
    """
    def __init__(self, call_id: int, parent_id: Optional[int], func_name: str, args: Dict[str, Any], depth: int):
        self.call_id = call_id
        self.parent_id = parent_id
        self.func_name = func_name
        self.args = args
        self.depth = depth
        self.return_value: Any = None
        self.children: List[TreeNode] = []
        self.status: str = "pending"  # "pending", "active", "completed"
        self.x: float = 0.0
        self.y: float = 0.0

    def format_args(self) -> str:
        items = []
        for k, v in self.args.items():
            if isinstance(v, list) and len(v) > 4:
                v_str = f"[{v[0]}..{v[-1]}]"
            else:
                v_str = repr(v)
            items.append(f"{k}={v_str}")
        return ", ".join(items)

    def label(self) -> str:
        """Short label for display inside node."""
        arg_str = self.format_args()
        lbl = f"{self.func_name}({arg_str})"
        if self.status == "completed" and self.return_value is not None:
            lbl += f"\n= {self.return_value}"
        return lbl


class RecursionTreeModel:
    """
    Manages the complete recursion tree structure and updates dynamic node states
    based on playback step index.
    """

    def __init__(self, events: List[TraceEvent]):
        self.events = events
        self.nodes: Dict[int, TreeNode] = {}
        self.root: Optional[TreeNode] = None
        self._build_tree_structure()
        self.compute_layout()

    def _build_tree_structure(self) -> None:
        """Constructs full node graph from CALL events."""
        self.nodes.clear()
        self.root = None

        # Create nodes for all call events
        for ev in self.events:
            if ev.is_call and ev.call_id not in self.nodes:
                node = TreeNode(
                    call_id=ev.call_id,
                    parent_id=ev.parent_id,
                    func_name=ev.func_name,
                    args=ev.args,
                    depth=ev.depth
                )
                self.nodes[ev.call_id] = node
                if ev.parent_id is None:
                    self.root = node

        # Link parent-children
        for node in self.nodes.values():
            if node.parent_id is not None and node.parent_id in self.nodes:
                parent = self.nodes[node.parent_id]
                if node not in parent.children:
                    parent.children.append(node)

    def compute_layout(self) -> None:
        """
        Computes (x, y) coordinates for all nodes in the tree.
        Uses a tidy tree layout algorithm based on subtree widths.
        """
        if not self.root:
            return

        # Y position: root at y = 0, decreasing with depth
        # Calculate sub-tree leaf width for X positioning
        leaf_counter = 0

        def layout_subtree(node: TreeNode, current_depth: int) -> float:
            nonlocal leaf_counter
            node.y = -float(current_depth)

            if not node.children:
                node.x = float(leaf_counter)
                leaf_counter += 1
                return node.x

            child_xs = []
            for child in node.children:
                child_xs.append(layout_subtree(child, current_depth + 1))

            # Center parent over children
            node.x = sum(child_xs) / len(child_xs)
            return node.x

        layout_subtree(self.root, 1)

    def get_state_at_step(self, step_idx: int) -> Tuple[List[TreeNode], List[TreeNode], Optional[TreeNode], Dict[str, Any]]:
        """
        Computes the state of the tree and call stack at a specific step index.

        Args:
            step_idx: Index of trace event (0-indexed). 0 means step 0 (first event),
                      len(events)-1 is the last step. -1 is before any event.

        Returns:
            Tuple containing:
                - visible_nodes: List of nodes created up to step_idx
                - active_stack: List of nodes currently in open active call stack
                - active_node: The node currently executing/returning at step_idx
                - metrics: Dictionary of current execution metrics
        """
        if not self.events or step_idx < 0:
            return [], [], None, {
                "total_calls": 0,
                "completed_calls": 0,
                "current_depth": 0,
                "max_depth": 0
            }

        # Clamp step_idx
        clamped_step = min(max(0, step_idx), len(self.events) - 1)

        # Re-set node states
        for node in self.nodes.values():
            node.status = "pending"
            node.return_value = None

        created_node_ids = set()
        completed_node_ids = set()
        active_stack_ids: List[int] = []
        max_depth_seen = 0

        for i in range(clamped_step + 1):
            ev = self.events[i]
            if ev.is_call:
                created_node_ids.add(ev.call_id)
                active_stack_ids.append(ev.call_id)
                if ev.depth > max_depth_seen:
                    max_depth_seen = ev.depth
            elif ev.is_return:
                completed_node_ids.add(ev.call_id)
                if ev.call_id in self.nodes:
                    self.nodes[ev.call_id].return_value = ev.return_value
                if active_stack_ids and active_stack_ids[-1] == ev.call_id:
                    active_stack_ids.pop()

        current_event = self.events[clamped_step]
        active_node_id = current_event.call_id if current_event else None
        active_node = self.nodes.get(active_node_id) if active_node_id else None

        # Apply visual statuses to created nodes
        visible_nodes = []
        for call_id in created_node_ids:
            if call_id in self.nodes:
                node = self.nodes[call_id]
                visible_nodes.append(node)
                if call_id in completed_node_ids:
                    node.status = "completed"
                else:
                    node.status = "pending"

        # The active node at current step
        if active_node and active_node in visible_nodes:
            active_node.status = "active"

        active_stack_nodes = [self.nodes[cid] for cid in active_stack_ids if cid in self.nodes]

        metrics = {
            "total_calls": len(created_node_ids),
            "completed_calls": len(completed_node_ids),
            "current_depth": len(active_stack_nodes),
            "max_depth": max_depth_seen
        }

        return visible_nodes, active_stack_nodes, active_node, metrics
