# Recursion Visualizer — Architecture & System Design

## Overview

**Recursion Visualizer** is built using a strict Model-View-Controller (MVC) architectural pattern. The core execution tracing engine is decoupled from the user interface, ensuring that algorithm logic can be tested independently in non-GUI test suites while rendering step-by-step visualizations in Tkinter and Matplotlib.

---

## High-Level Data Flow Architecture

```
+--------------------------+
|  User / GUI Controls     |
+-------------+------------+
              | (Triggers execution)
              v
+--------------------------+
|  Recursive Algorithm     |  (e.g., Fibonacci, Factorial, Binary Search, N-Queens)
+-------------+------------+
              | (Emits record_call / record_return)
              v
+--------------------------+
|    RecursionTracer       |  (Validates limits, assigns call_id, builds events)
+-------------+------------+
              | (Produces List[TraceEvent])
              v
+--------------------------+
|   RecursionTreeModel     |  (Calculates tree 2D layout & reconstructs state per step)
+-------------+------------+
              | (Provides node states & call stack frames)
              v
+--------------------------+
|   PlaybackController     |  (Manages step index, play/pause, speed, notifies views)
+-------------+------------+
              | (Triggers UI updates via Tkinter main loop)
              v
+-----------------------------------------------------------------+
|                         UI Views                                |
|  +-----------------------------+  +--------------------------+  |
|  | Matplotlib Tree / N-Queens  |  |   CallStackView Tree     |  |
|  +-----------------------------+  +--------------------------+  |
+-----------------------------------------------------------------+
```

---

## Core Components

### 1. Tracing Engine (`core/tracer.py` & `core/events.py`)
- **`TraceEvent`**: Immutable data container capturing execution state (`CALL` / `RETURN`, `call_id`, `parent_id`, `func_name`, `args`, `depth`, `return_value`, `seq_num`, `extra_info`).
- **`RecursionTracer`**: Manages event capture during algorithm execution. Maintains an internal call stack to map child calls to parent IDs without using global Python hooks. Implements a configurable event safety cap (`max_events=5000`) to prevent GUI locks or infinite stack overflows.

### 2. Tree Data Model & Layout (`core/tree_model.py`)
- **`TreeNode`**: Graph representation of function calls.
- **`RecursionTreeModel`**: Reconstructs tree structure from event traces. Computes `(x, y)` 2D layout coordinates dynamically:
  - **Y-coordinate**: Inversely proportional to recursion depth (`y = -depth`).
  - **X-coordinate**: Calculated using a tidy subtree leaf-width algorithm to ensure child nodes center cleanly under parents without sibling overlaps.
- **`get_state_at_step(step_idx)`**: Evaluates active, completed, and pending node states up to step index `step_idx`.

### 3. Playback Controller (`core/playback.py`)
- State machine managing execution timeline navigation (`step_forward`, `step_backward`, `play`, `pause`, `reset`, `go_to_step`).
- Decoupled from Tkinter timers; uses observer pattern listeners to broadcast step state changes.

### 4. UI Layer (`ui/`)
- **`RecursionVisualizerApp`** (`ui/app.py`): Main window container, handles dark theme styling, layout split panels, and drives non-blocking auto-play using Tkinter's `after()` loop.
- **`TreeVisualizerCanvas`** (`ui/tree_view.py`): Embedded Matplotlib figure for displaying recursive call graphs with distinct color states (Active: gold/orange, Completed: green, Pending: gray).
- **`NQueensCanvas`** (`ui/n_queens_view.py`): Dedicated Tkinter canvas board for displaying chessboard configurations, row/column exploration, and queen placement vectors.
- **`CallStackView`** (`ui/stack_view.py`): Highlights active stack frames with top-of-stack frame emphasized.
- **`ControlPanel`** (`ui/controls.py`): Dynamic input fields per algorithm, playback controls, and speed settings.

---

## Threading & GUI Responsiveness

- All algorithm trace recording executes synchronously prior to playback.
- Auto-play uses Tkinter's event-driven `after(delay_ms, callback)` scheduler rather than blocking `time.sleep()`, guaranteeing a 100% responsive GUI thread.
