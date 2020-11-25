"""
This module defines the buffer class, used to buffer print operations.

TODO:
- RGB color support
- Buffer delta to only update parts
- use wcwidth instead of len
"""
import sys
from typing import List


class Buffer:
    """A simple text buffer."""

    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._buffer: List[str] = [" " * width for i in range(height)]

    def set_size(self, width: int, height: int) -> None:
        """Resize the buffer"""
        new_buffer = []
        for y in range(height):
            old_line = self._buffer[y] if y < self._height else ""
            new_buffer.append(old_line[:width] + "X" * (max(width - self._width, 0)))
        self._width = width
        self._height = height
        self._buffer = new_buffer

    def draw_text(self, x, y, text: str) -> None:
        """Draw some text in the buffer."""
        if y >= self._height or y < 0:
            return
        if x >= self._width:
            return
        line = self._buffer[y]
        newline = line[:x] + text + line[x + len(text) :]
        self._buffer[y] = newline[: self._width]

    def clear(self) -> None:
        """Clear the buffer."""
        for y in range(self._height):
            self._buffer[y] = " " * self._width

    def flush(self) -> None:
        """Flush the buffer's contents to the screen."""
        sys.stdout.write("\x1b[2J")
        sys.stdout.write("\x1b[H")
        sys.stdout.writelines(self._buffer)
        sys.stdout.flush()
