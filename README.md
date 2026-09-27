# 🌳 Recursion Visualizer

An interactive desktop application built with Python, Tkinter, and Matplotlib to trace, step through, and visualize recursive Data Structures & Algorithms (DSA) execution in real-time.

![Recursion Visualizer Tree View](docs/screenshots/tree_view_placeholder.png)
![Recursion Visualizer N-Queens View](docs/screenshots/n_queens_view_placeholder.png)

---

## 🌟 Key Features

* **Deterministic Tracing Engine**: Captures real execution events (`CALL` and `RETURN`) with exact function parameters, recursion depth, and return propagation.
* **Dual-Panel Visualization**:
  * **Left Panel**: Interactive Recursion Tree graph rendered via embedded Matplotlib, or a dedicated Tkinter Canvas chessboard for N-Queens.
  * **Right Panel**: Real-time Call Stack display with top stack frame highlighting.
* **Complete Playback Controls**: Step forward, step backward, auto-play, pause, reset, and dynamic speed adjustment (Slow, Normal, Fast, Ultra).
* **Metrics & Analytics**: Tracks total calls, current recursion depth, max recursion depth, completed calls, and algorithm status.
* **Input Validation & Safety**: Includes maximum event guards (`max_events`) to prevent UI freezes or stack overflow crashes on large inputs.
* **Modern Dark Theme**: Designed with custom palette styling for readability and clean presentation.

---

## 🛠️ Technology Stack

* **Language**: Python 3.11+ (Tested on Python 3.13)
* **GUI Framework**: Tkinter & `ttk` (Python Standard Library)
* **Visualization**: Matplotlib embedded via `FigureCanvasTkAgg`
* **Testing Framework**: `pytest`

---

## 🚀 Installation & Setup

### Prerequisites
* Windows 10/11 (or macOS / Linux)
* Python 3.11 or later installed and added to system `PATH`

### Windows Setup Instructions

1. **Clone or Download the Repository**:
   ```cmd
   git clone https://github.com/YOUR_USERNAME/recursion-visualizer.git
   cd recursion-visualizer
   ```

2. **Create a Virtual Environment** (Optional but recommended):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

---

## 🎮 Running the Application

Launch the desktop GUI by executing `main.py`:

```cmd
python main.py
```

---

## 🧪 Running Automated Tests

Run the complete test suite with `pytest`:

```cmd
python -m pytest -v
```

---

## 🧮 Supported Algorithms & Complexities

| Algorithm | Function Signature | Time Complexity | Space Complexity (Recursion Depth) | Description |
|---|---|---|---|---|
| **Fibonacci** | `fib(n)` | $\mathcal{O}(2^n)$ | $\mathcal{O}(n)$ | Traces overlapping subproblems and binary recursive tree structure. |
| **Factorial** | `factorial(n)` | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Visualizes linear recursion chain, base case hit, and return value propagation. |
| **Binary Search** | `binary_search(arr, low, high, target)` | $\mathcal{O}(\log n)$ | $\mathcal{O}(\log n)$ | Demonstrates divide-and-conquer search interval halving on a sorted list. |
| **N-Queens** | `solve_n_queens(n)` | $\mathcal{O}(N!)$ | $\mathcal{O}(N)$ | Visualizes N-Queens backtracking solver step-by-step on a chessboard canvas. |

---

## 📁 Project Structure

```
recursion-visualizer/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── algorithms/
│   ├── __init__.py
│   ├── fibonacci.py
│   ├── factorial.py
│   ├── binary_search.py
│   └── n_queens.py
├── core/
│   ├── __init__.py
│   ├── events.py
│   ├── tracer.py
│   ├── tree_model.py
│   └── playback.py
├── ui/
│   ├── __init__.py
│   ├── app.py
│   ├── tree_view.py
│   ├── stack_view.py
│   ├── controls.py
│   └── n_queens_view.py
├── tests/
│   ├── __init__.py
│   ├── test_fibonacci.py
│   ├── test_factorial.py
│   ├── test_binary_search.py
│   ├── test_n_queens.py
│   └── test_tracer.py
└── docs/
    └── architecture.md
```

---

## 🏗️ Architecture Summary

The application follows strict Model-View-Controller (MVC) separation:
* **Core Tracing Engine** (`core/tracer.py`): Records deterministic `CALL` and `RETURN` events during algorithm execution without relying on Tkinter.
* **Tree Model** (`core/tree_model.py`): Computes 2D spatial coordinates for recursion tree nodes and tracks node visual states (`active`, `completed`, `pending`).
* **Playback Controller** (`core/playback.py`): Manages playback index stepping and subscriber updates.
* **UI Views** (`ui/`): Renders Matplotlib tree graph, Call Stack Treeview, and N-Queens board canvas asynchronously using Tkinter `after()` loops.

For comprehensive architectural documentation, see [docs/architecture.md](docs/architecture.md).

---

## 🔮 Future Improvements

* Add support for Merge Sort and Quick Sort array partition visualizers.
* Export execution traces to JSON or animated GIF/MP4 format.
* Add zoom/pan controls for extremely large recursion trees.
* Support custom user-defined recursive Python code snippet tracing.

---

## 🐙 Git & GitHub Commands for Publishing

Execute the following commands in your terminal to initialize Git and push the repository to your GitHub account:

```cmd
git init
git add .
git commit -m "Initial commit: Recursion Visualizer desktop app with full test suite"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/recursion-visualizer.git
git push -u origin main
```

---

## 📄 License & Author

Distributed under the MIT License. See `LICENSE` for more information.

**Author**: CS Portfolio Project / Maintainer
