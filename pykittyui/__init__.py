import termios
from typing import Sequence

from .keys import KeyCombo
from .buffer import Buffer

class Window:
    """A terminal GUI."""
    def __init__(self) -> None:
        self._should_run: bool = False
        self._width: int = 0
        self._height: int = 0
        self._buffer = Buffer(0, 0)

    def get_buffer(self) -> Buffer:
        return self._buffer

    def on_key(self, combo: KeyCombo) -> None:
        """Handle a key press."""

    def quit(self) -> None:
        """Stop the running app."""
        self._should_run = False

    def draw(self, width: int, height: int) -> None:
        """Draw the contents of the window."""

    def loop(self) -> None:
        """Run the main loop."""
        self._should_run = True
        while self._should_run:
            pass

    def __del__(self) -> None:
        """Cleanup on destroy."""
        # TODO disable direct mode
