"""
PyKittyUi is a terminal ui helper made for Kitty.
"""

from abc import ABC, abstractmethod
import atexit
from queue import Queue
from shutil import get_terminal_size
import signal
import sys
import termios
from typing import Sequence, Tuple, Union

from pykittyui.buffer import Buffer
import pykittyui.events as events
from pykittyui.keys import KeyEvent, read_keys


class Window(ABC):
    """A terminal GUI."""

    def __init__(self) -> None:
        self._width: int = 80
        self._height: int = 24
        self._buffer = Buffer(80, 24)
        self._event_queue: "Queue[events.Event]" = Queue()
        atexit.register(self._cleanup)

    def queue_event(self, event: events.Event) -> None:
        """Put an event at the end of the queue."""
        self._event_queue.put(event)

    def get_buffer(self) -> Buffer:
        """Return the internal buffer."""
        return self._buffer

    def get_dimensions(self) -> Tuple[int, int]:
        """Return the width and height of this window."""
        return self._width, self._height

    @abstractmethod
    def on_key(self, combo: KeyEvent) -> None:
        """Handle a key press."""

    def quit(self) -> None:
        """Stop the running app."""
        self.queue_event(events.QuitEvent())

    def redraw(self) -> None:
        """Redraw the screen."""
        self.queue_event(events.RedrawEvent())

    def on_resize(self, width: int, height: int) -> None:
        """When the terminal was resized."""
        self._width = width
        self._height = height
        self._buffer.set_size(width, height)
        self.queue_event(events.RedrawEvent())

    def _sigwinch_handler(self, sig: signal.Signals, _frame) -> None:
        """Handle the terminal resize signal."""
        if sig != signal.SIGWINCH:
            return
        self.queue_event(events.ResizeEvent())

    @abstractmethod
    def draw(self) -> None:
        """Draw the contents of the window."""

    def loop(self) -> None:
        """Run the main loop."""
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
        while True:
            event = self._event_queue.get()
            if isinstance(event, KeyEvent):
                self.on_key(event)
            elif isinstance(event, events.ResizeEvent):
                self.on_resize(*get_terminal_size(self.get_dimensions()))
            elif isinstance(event, events.QuitEvent):
                break
            elif isinstance(event, events.RedrawEvent):
                self.draw()
                self._buffer.flush()
            else:
                raise RuntimeError("Unhandled event.")

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
