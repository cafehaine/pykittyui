from abc import ABC

class Event(ABC):
    """The base event class."""

class QuitEvent(Event):
    """Signal that the program should exit."""

class ResizeEvent(Event):
    """Signal that the terminal was resized."""

class RedrawEvent(Event):
    """Signal that the contents should be redrawn."""
