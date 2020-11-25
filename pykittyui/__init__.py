import atexit
from queue import Queue
import sys
import termios
from typing import Sequence, Tuple

from .keys import KeyCombo, read_keys
from .buffer import Buffer


class Window:
    """A terminal GUI."""

    def __init__(self) -> None:
        self._should_run: bool = False
        self._width: int = 80
        self._height: int = 40
        self._buffer = Buffer(80, 40)
        atexit.register(self._cleanup)

    def get_buffer(self) -> Buffer:
        """Return the internal buffer."""
        return self._buffer

    def get_dimensions(self) -> Tuple[int, int]:
        """Return the width and height of this window."""
        return self._width, self._height

    def on_key(self, combo: KeyCombo) -> None:
        """Handle a key press."""

    def quit(self) -> None:
        """Stop the running app."""
        self._should_run = False

    def on_resize(self, width: int, height: int) -> None:
        """When the terminal was resized."""
        self._width = width
        self._height = height
        self._buffer.set_size(width, height)

    def draw(self) -> None:
        """Draw the contents of the window."""

    def loop(self) -> None:
        """Run the main loop."""
        self._should_run = True
        # Enable kitty full mode
        sys.stdout.write("\x1b[?2017h")
        sys.stdout.flush()
        # Disable key echo
        attrs = termios.tcgetattr(sys.stdin)
        attrs[3] = attrs[3] & (~(termios.ECHO | termios.ICANON))
        termios.tcsetattr(sys.stdin, termios.TCSANOW, attrs)

        key_queue: "Queue[KeyCombo]" = Queue()
        read_keys(key_queue)

        self.draw()
        self._buffer.flush()
        while self._should_run:
            self.on_key(key_queue.get())
            self.draw()
            self._buffer.flush()

    @staticmethod
    def _cleanup() -> None:
        """Cleanup on destroy."""
        # Disable kitty full mode
        sys.stdout.write("\x1b[?2017l")
        sys.stdout.flush()
        # Enable key echo
        attrs = termios.tcgetattr(sys.stdin)
        attrs[3] = attrs[3] | termios.ECHO | termios.ICANON
        termios.tcsetattr(sys.stdin, termios.TCSANOW, attrs)
