import atexit
from queue import Queue
from shutil import get_terminal_size
import signal
import sys
import termios
from typing import Sequence, Tuple, Union

from .keys import KeyCombo, read_keys
from .buffer import Buffer


class WindowResizeEvent:
    """Sent when the window was resized."""


class Window:
    """A terminal GUI."""

    def __init__(self) -> None:
        self._should_run: bool = False
        self._width: int = 80
        self._height: int = 24
        self._buffer = Buffer(80, 24)
        self._event_queue: "Queue[Union[KeyCombo, WindowResizeEvent]]" = Queue()
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

    def _sigwinch_handler(self, sig: signal.Signals, frame) -> None:
        """Handle the terminal resize signal."""
        if sig != signal.SIGWINCH:
            return
        self._event_queue.put(WindowResizeEvent())

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
        # Register handler for SIGWINCH
        signal.signal(signal.SIGWINCH, self._sigwinch_handler)

        # Re-initialise buffer with correct dimensions
        self.on_resize(*get_terminal_size(self.get_dimensions()))

        read_keys(self._event_queue)

        self.draw()
        self._buffer.flush()
        while self._should_run:
            event = self._event_queue.get()
            if isinstance(event, KeyCombo):
                self.on_key(event)
            elif isinstance(event, WindowResizeEvent):
                self.on_resize(*get_terminal_size(self.get_dimensions()))
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
