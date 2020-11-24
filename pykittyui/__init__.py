import atexit
from queue import Queue
import sys
import termios
from typing import Sequence

from .keys import KeyCombo, read_keys
from .buffer import Buffer

class Window:
    """A terminal GUI."""
    def __init__(self) -> None:
        self._should_run: bool = False
        self._width: int = 0
        self._height: int = 0
        self._buffer = Buffer(0, 0)
        atexit.register(self._cleanup)

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
        # Enable kitty full mode
        sys.stdout.write("\x1b[?2017h")
        sys.stdout.flush()
        # Disable key echo
        attrs = termios.tcgetattr(sys.stdin)
        attrs[3] = attrs[3] & (~(termios.ECHO | termios.ICANON))
        termios.tcsetattr(sys.stdin, termios.TCSANOW, attrs)
        self.draw(80, 40) # TODO use real width

        key_queue: 'Queue[KeyCombo]' = Queue()
        read_keys(key_queue)

        while self._should_run:
            print("{}".format(key_queue.get()))

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
