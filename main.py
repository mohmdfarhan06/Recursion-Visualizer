"""
Main entry point for the Recursion Visualizer application.
"""

import sys
from ui.app import RecursionVisualizerApp


def main():
    """Launches the desktop application."""
    app = RecursionVisualizerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
